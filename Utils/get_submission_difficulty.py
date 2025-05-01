import requests
import json
from get_submissions import get_submissions

def get_submission_difficulty(username, timestamp):
    submissions = get_submissions(username, timestamp)
    if submissions is None:
        print("Failed to fetch submissions.")
        return None

    AC_LIST, WA_LIST, OTHERS_LIST = [], [], []

    for s in submissions:
        match s.get("result"):
            case "AC":
                AC_LIST.append(s)
            case "WA":
                WA_LIST.append(s)
            case _:
                OTHERS_LIST.append(s)

    print(f"AC数: {len(AC_LIST)}, WA数: {len(WA_LIST)}, OTHERS数: {len(OTHERS_LIST)}")

    return {
        "AC": AC_LIST,
        "WA": WA_LIST,
        "OTHERS": OTHERS_LIST,
    }

# get_submission_difficulty("ritsuepi", 0)