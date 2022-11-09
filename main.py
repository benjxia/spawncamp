import requests
import json
import browser_cookie3
import time
from winotify import Notification, audio

course_dep = "CSE"
# If < 100, +X, if < 10, ++X
course_num = "151A"

# Desktop notification setup
OPENING_NOTIFY = Notification(app_id="SPAWNCAMP",
                    title="OPENING FOUND",
                    msg="WAKE THE FUCK UP",
                    duration="long")

OPENING_NOTIFY.set_audio(audio.LoopingAlarm, loop=True)

RESET_COOKIES = Notification(app_id="SPAWNCAMP",
                             title="RESET CHROME COOKIES",
                             msg="WAKE THE FUCK UP",
                             duration="long")
RESET_COOKIES.set_audio(audio.LoopingAlarm, loop=True)

# Grab cookies from chrome for login credentials
cookies = browser_cookie3.chrome(domain_name='.ucsd.edu')
cookie_dict = dict()
for i in cookies:
    cookie_dict[i.name] = i.value
    pass

prev = None

while True:
    # HTTP GET for class info
    request_out = requests.get(f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode={course_dep}&crsecode={course_num}&termcode=WI23", cookies=cookie_dict)
    try:
        request_json = json.loads(request_out.text)
    except json.decoder.JSONDecodeError:
        RESET_COOKIES.show()
        exit(1)

    # If no change -> no notification
    if prev == request_json:
        print("no change :(")
        print("-------------------------------")
        time.sleep(1)
        continue

    # Update prev in case of update
    prev = request_json
    n = len(request_json)
    # # of sections with available seats
    cnt = 0
    for i in range(n):
        if request_json[i]['AVAIL_SEAT'] != request_json[i]['SCTN_CPCTY_QTY'] and int(request_json[i]['AVAIL_SEAT']) > 0:
            print(f"Section: {request_json[i]['SECT_CODE']} Seats: {request_json[i]['AVAIL_SEAT']}")
            # Show desktop notification
            cnt += 1
    if cnt != 0:
        OPENING_NOTIFY.msg = f"OPENING FOUND IN {course_dep} {course_num}"
        OPENING_NOTIFY.show()

    print("-------------------------------")

    # Avoid getting FBI'd for DDoSing
    time.sleep(1)
