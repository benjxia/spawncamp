# Written by Benjamin Xia 笨虾
# December 14, 2022
# 我的脑子很小。

import requests
import json
import browser_cookie3
import time
from winotify import Notification, audio
import sys

def enroll(SECT_ID: str, COURSE_DEPT: str, COURSE_CODE: str, TERM_CODE: str, UNIT_CNT: str):
    # Grab cookies from chrome for login credentials
    cookies = browser_cookie3.chrome(domain_name='.ucsd.edu')
    cookie_dict = dict()
    for i in cookies:
        cookie_dict[i.name] = i.value

    # response = requests.post()


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