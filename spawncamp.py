import requests
import json
import browser_cookie3
import time
from winotify import Notification, audio

# EDIT THIS
COURSE_DEPT = "CSE"
COURSE_CODE = "151A"

# Notification stuff, avoid editing unless you hate the sound or are on mac
OPENING_NOTIFY = Notification(app_id = "SPAWNCAMP",
                              title = "COURSE OPENING FOUND",
                              msg = "GET ON WEGREG (placeholder)",
                              duration = "long")
OPENING_NOTIFY.set_audio(audio.LoopingAlarm, loop = True)

RESET_COOKIES = Notification(app_id="SPAWNCAMP",
                             title="RESET CHROME COOKIES",
                             msg="Sign back into Webreg on Chrome",
                             duration="long")
RESET_COOKIES.set_audio(audio.LoopingAlarm8, loop = True)


# Grab cookies from chrome for login credentials
cookies = browser_cookie3.chrome(domain_name='.ucsd.edu')
cookie_dict = dict()
for i in cookies:
    cookie_dict[i.name] = i.value
    
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

# Previous JSON output from HTTP get
prev = None
HTTP_GET_URL = f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode={COURSE_DEPT}&crsecode={parse_course_num(COURSE_CODE)}&termcode=WI23"


if __name__ == "__main__":
    while True:
        requests_out = requests.get(HTTP_GET_URL, cookies = cookie_dict)
        requests_json = []
        try:
            requests_json = json.loads(requests_out.text)
        except json.decoder.JSONDecodeError:
            RESET_COOKIES.show()
            exit(1)

        # No output if no change
        if prev == requests_json:
            time.sleep(1)
            continue
        
        prev = requests_json
        cnt = 0
        for i in range(len(requests_json)):
            if requests_json[i]['AVAIL_SEAT'] != requests_json[i]['SCTN_CPCTY_QTY'] and int(requests_json[i]['AVAIL_SEAT']) > 0:
                print(f"Section: {requests_json[i]['SECT_CODE']} Seats: {requests_json[i]['AVAIL_SEAT']}")
                # Show desktop notification
                cnt += 1
                
        if cnt != 0:
            OPENING_NOTIFY.msg = f"OPENING FOUND IN {COURSE_DEPT} {COURSE_CODE}"
            OPENING_NOTIFY.show()
            print("------------------------------------------")
        
        time.sleep(1)

        