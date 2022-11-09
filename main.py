import requests
import json
import browser_cookie3
import time
from winotify import Notification, audio

# Desktop notification setup
test = Notification(app_id="SPAWNCAMP",
                    title="OPENING FOUND",
                    msg="WAKE THE FUCK UP",
                    duration="long")
test.set_audio(audio.LoopingAlarm, loop=True)

# Grab cookies from chrome for login credentials
cookies = browser_cookie3.chrome(domain_name='.ucsd.edu')
cookie_dict = dict()
for i in cookies:
    cookie_dict[i.name] = i.value
    pass

prev = None

while True:
    # HTTP GET for class info
    request_out = requests.get("https://act.ucsd.edu/webreg2/svc/wradapter/secure/search-load-group-data?subjcode=CSE&crsecode=151A&termcode=WI23", cookies=cookie_dict)
    request_json = json.loads(request_out.text)
    
    # If no change -> no notification
    if prev == request_json:
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
            test.show()
            cnt += 1
    if cnt == 0:
        print("Nothing :(")
        
    print("-------------------------------")
    
    # Avoid getting FBI'd for DDoSing
    time.sleep(1)
