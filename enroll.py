# Written by Benjamin Xia 笨虾
# December 14, 2022
# 我的脑子很小。

import requests
import json
import browser_cookie3
import time
from winotify import Notification, audio

# EDIT THIS
COURSE_DEPT = "CSE"
COURSE_CODE = "141L"
TERM_CODE = "WI23"  # ex. FA22 WI23 SP23 S123 S223
SECT_NUM = "102342"
SECT_CODE = "A01"


cookies = browser_cookie3.chrome(domain_name = '.ucsd.edu')
cookie_dict = dict()
for i in cookies:
    cookie_dict[i.name] = i.value


HTTP_POST_URL = f"https://act.ucsd.edu/webreg2/svc/wradapter/secure/add-enroll?section=098779&grade=L&unit=2.00&subjcode=PHYS&crsecode=++2CL&termcode=WI23"


request_json = requests.post(HTTP_POST_URL, cookies= cookie_dict)
print(request_json)


# if __name__ == "__main__":
#     while True:
#         # Fetch info from webreg
#         requests_out = requests.get(HTTP_GET_URL, cookies = cookie_dict)
#         requests_json = []
#         try:
#             requests_json = json.loads(requests_out.text)
#         except json.decoder.JSONDecodeError: # Only happens when cookies expire, sign back into webreg!
#             RESET_COOKIES.show()
#             exit(1)

#         # No output if no change from previous fetch
#         if prev == requests_json:
#             time.sleep(1)
#             continue
        
#         prev = requests_json
#         cnt = 0
#         # See if any sections have open seats and print the sections with open spots. 
#         for i in range(len(requests_json)):
#             if requests_json[i]['AVAIL_SEAT'] != requests_json[i]['SCTN_CPCTY_QTY'] and int(requests_json[i]['AVAIL_SEAT']) > 0:
#                 print(f"Section: {requests_json[i]['SECT_CODE']} Seats: {requests_json[i]['AVAIL_SEAT']}")
#                 # Show desktop notification
#                 cnt += 1
        
#         # Make notification if opening in a section. 
#         if cnt != 0:
#             OPENING_NOTIFY.msg = f"OPENING FOUND IN {COURSE_DEPT} {COURSE_CODE}"
#             OPENING_NOTIFY.show()
#             print("------------------------------------------")
        
#         # Avoid getting FBI'd for Ddosing webreg. 
#         time.sleep(1)
