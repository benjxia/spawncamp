# Written by Benjamin Xia 笨虾
# November 8, 2022
# 我的脑子很小。

import json
import time
import os
import sys

# EDIT THIS
COURSE_DEPT = "PHYS"
COURSE_CODE = "2CL"
TERM_CODE = "FA23"  # ex. FA22 WI23 SP23 S123 S223
SECTION_ID = {"247730"}  # List of section ID's to enroll in
UNIT_CNT = "2.00"  # ex. 4.00 for 4 unit courses

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip3", "install", 'requests'])
finally:
    import requests

try:
    import browser_cookie3
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip3", "install", 'browser-cookie3'])
finally:
    import browser_cookie3

# Grab cookies from chrome for login credentials
try:
    cookies = browser_cookie3.chrome(domain_name='.ucsd.edu')
except PermissionError:
    print("Permission Error - Please close Chrome so I can access your browser cookies, you may reopen it after launching the script.", file=sys.stderr)
    exit(1)

cookie_dict = dict()
for i in cookies:
    cookie_dict[i.name] = i.value

if sys.platform.startswith("win32"):
    # Import dependencies
    try:
        from winotify import Notification, audio
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip3", "install", 'winotify'])
    finally:
        from winotify import Notification, audio

    # Notification stuff, avoid editing unless you hate the sound or are on mac
    ENROLLMENT_NOTIFY = Notification(app_id="Spawncamp",
                                     title="Enrollment Successful!",
                                     msg=f"Enrollment into {COURSE_DEPT} {COURSE_CODE} successful!",
                                     duration="long")
    ENROLLMENT_NOTIFY.set_audio(audio.LoopingAlarm, loop=True)

    # Webreg requires you to be signed in in order to receive any information
    # This script uses your existing chrome cookies as authentication.
    # Webreg automatically signs you out after some time, so you will need to
    # sign back in when the notification pops up.
    RESET_COOKIES = Notification(app_id="Spawncamp",
                                 title="Cookies Expired",
                                 msg="Sign back into Webreg on Chrome",
                                 duration="long")
    RESET_COOKIES.set_audio(audio.LoopingAlarm8, loop=True)


# Notifications on MacOS
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def show_cookie_error():
    if sys.platform.startswith("win32"):
        RESET_COOKIES.show()
    else:
        notify("Spawncamp", "Sign back into Webreg on Chrome")


def show_enroll_success():
    if sys.platform.startswith("win32"):
        ENROLLMENT_NOTIFY.show()
    else:
        notify("Spawncamp", "Enrollment Successful in " + COURSE_DEPT + " " + COURSE_CODE + "!")


def enroll(SECT_ID: str, COURSE_DEPT: str, COURSE_CODE: str, TERM_CODE: str, UNIT_CNT: str,
           cookie_dict: dict[str, str]) -> int:
    """
    Attempts to enroll in the specified course

    Returns:
    The enrollment HTTP Post's response code
    """
    # Doing this extra edit-enroll HTTP POST is necessary, I don't know why
    HTTP_POST_URL_EDIT = f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/edit-enroll?section={SECT_ID}&subjcode={COURSE_DEPT}&crsecode={COURSE_CODE}&termcode={TERM_CODE}"
    requests.post(HTTP_POST_URL_EDIT, cookies=cookie_dict)
    HTTP_POST_URL_ENROLL = f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/add-enroll?section={SECT_ID}&grade=L&unit={UNIT_CNT}&subjcode={COURSE_DEPT}&crsecode={parse_course_num(COURSE_CODE)}&termcode={TERM_CODE}"
    response = requests.post(HTTP_POST_URL_ENROLL, cookies=cookie_dict)
    return response.status_code


def parse_course_num(code: str) -> str:
    """
    Webreg's API is dumb, so if we need a course with code
    151A, the parameter would be 151A, but if the number were < 100, we'd need
    +XX, ex. +15L for CSE 15L or +10 for MATH 10 or something. For < 10, we'd
    need ++, so ++1 for COGS 1.

    Arguments:
    code: Class code you want notifications for, like 101 for CSE 101.

    Returns:
    API compatible version of the course code
    """
    course_num = ""
    idx: int = 0
    for i in range(len(code)):
        if code[i].isdigit():
            course_num += code[i]
        else:
            idx = i
            break

    course_num = int(course_num)

    course_out = ""

    while course_num < 100:
        course_out += "+"
        course_num *= 10

    course_out += code[:idx]

    return course_out + code[idx:]


def cycle():
    global prev
    requests_out = requests.get(HTTP_GET_URL, cookies=cookie_dict)

    try:
        requests_json = json.loads(requests_out.text)
    except json.decoder.JSONDecodeError:  # Only happens when cookies expire, sign back into webreg!
        show_cookie_error()
        exit(1)

        # No output if no change from previous fetch
    if prev == requests_json:
        return

    prev = requests_json

    # See if any sections have open seats and print the sections with open spots.
    for i in range(len(requests_json)):
        # If current section has seats
        if requests_json[i]["AVAIL_SEAT"] != requests_json[i]["SCTN_CPCTY_QTY"] and int(
                requests_json[i]["AVAIL_SEAT"]) > 0:
            # IF OPENING IN CORRECT SECTION FOUND, ENROLL IN COURSE
            if requests_json[i]["SECTION_NUMBER"] in SECTION_ID:
                print("OPENING FOUND")
                res = enroll(requests_json[i]["SECTION_NUMBER"], COURSE_DEPT, COURSE_CODE, TERM_CODE, UNIT_CNT,
                             cookie_dict)
                if res == 200:
                    show_enroll_success()
                    exit(0)


HTTP_GET_URL = f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode={COURSE_DEPT}&crsecode={parse_course_num(COURSE_CODE)}&termcode={TERM_CODE}"

prev = None  # Previous JSON output from HTTP get

if __name__ == "__main__":
    print("Spawncamp is running...")
    while True:
        # Fetch info from webreg
        cycle()
        # Avoid getting FBI'd for Ddosing webreg.
        time.sleep(1)
