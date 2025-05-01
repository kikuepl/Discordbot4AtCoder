import requests
import json

def get_submission_difficulty(username, timestamp):
    #timestamp以降で500件のデータを取得 
    submissions_url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={timestamp}"
    problem_models_url = "https://kenkoooo.com/atcoder/resources/problem-models.json"

    submissions_response = requests.get(submissions_url)
    problem_models_response = requests.get(problem_models_url)

    if submissions_response.status_code == 200 and problem_models_response.status_code == 200:
        submissions = submissions_response.json()
        problem_models = problem_models_response.json()

        AC_LIST = []        #AC
        WA_LIST = []        #WA
        OTHERS_LIST = []    #エラーとか

        for s in submissions:
            if s.get("result") == "AC":
                AC_LIST.append(s)
            elif s.get("result") == "WA":
                WA_LIST.append(s)
            else:
                OTHERS_LIST.append(s)
        print(f"AC数: {len(AC_LIST)}, WA数: {len(WA_LIST)}, OTHERS数: {len(OTHERS_LIST)}")
        print(f"ACリスト: {AC_LIST}")
        print(f"WAリスト: {WA_LIST}")
        print(f"OTHERSリスト: {OTHERS_LIST}")
        
        return {AC_LIST, WA_LIST, OTHERS_LIST}