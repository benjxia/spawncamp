# Written by Benjamin Xia 笨虾
# November 8, 2022
# 我的脑子很小。

import requests
import json
import browser_cookie3
import time
from winotify import Notification, audio
from enroll import parse_course_num
from enroll import enroll


# EDIT THIS
COURSE_DEPT = "PHYS"
COURSE_CODE = "2CL"
TERM_CODE = "WI23"  # ex. FA22 WI23 SP23 S123 S223
SECTION_ID = ["098783", "098782"]  # List of section ID's to enroll in
UNIT_CNT = "2.00"

# Grab cookies from chrome for login credentials
cookies = browser_cookie3.chrome(domain_name='.ucsd.edu')
cookie_dict = dict()
for i in cookies:
    cookie_dict[i.name] = i.value

# Notification stuff, avoid editing unless you hate the sound or are on mac
ENROLLMENT_NOTIFY = Notification(app_id="SPAWNCAMP",
                                 title="ENROLLMENT SUCCESSFUL",
                                 msg="Enrollment worked :)",
                                 duration="long")
ENROLLMENT_NOTIFY.set_audio(audio.LoopingAlarm, loop=True)

# Webreg requires you to be signed in in order to receive any information
# This script uses your existing chrome cookies as authentication.
# Webreg automatically signs you out after some time, so you will need to
# sign back in when the notification pops up.
RESET_COOKIES = Notification(app_id="SPAWNCAMP",
                             title="RESET CHROME COOKIES",
                             msg="Sign back into Webreg on Chrome",
                             duration="long")
RESET_COOKIES.set_audio(audio.LoopingAlarm8, loop=True)

prev = None  # Previous JSON output from HTTP get

COURSE_CODE = parse_course_num(COURSE_CODE)

HTTP_GET_URL = f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode={COURSE_DEPT}&crsecode={COURSE_CODE}&termcode={TERM_CODE}"

if __name__ == "__main__":
    while True:
        # Fetch info from webreg
        requests_out = requests.get(HTTP_GET_URL, cookies=cookie_dict)
        requests_json = []
        try:
            requests_json = json.loads(requests_out.text)
        except json.decoder.JSONDecodeError:  # Only happens when cookies expire, sign back into webreg!
            RESET_COOKIES.show()
            exit(1)

        # No output if no change from previous fetch
        if prev == requests_json:
            time.sleep(1)
            continue

        prev = requests_json
        cnt = 0

        # See if any sections have open seats and print the sections with open spots. 
        for i in range(len(requests_json)):
            # If current section has seats
            if requests_json[i]["AVAIL_SEAT"] != requests_json[i]["SCTN_CPCTY_QTY"] and int(
                    requests_json[i]["AVAIL_SEAT"]) > 0:
                # IF OPENING IN CORRECT SECTION FOUND, ENROLL IN COURSE
                if requests_json[i]["SECTION_NUMBER"] in SECTION_ID:
                    print("OPENING FOUND")
                    SECT = requests_json[i]["SECTION_NUMBER"]
                    # Insert enrollment script here

        # Avoid getting FBI'd for Ddosing webreg. 
        time.sleep(1)
