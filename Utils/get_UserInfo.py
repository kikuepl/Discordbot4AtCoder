import requests
import json

PROXY_API_URL = "https://kenkoooo.com/atcoder/proxy"

def UserInfo(username):
    #timestamp以降で500件のデータを取得 
    url = f"{PROXY_API_URL}/users/{username}/history/json"
    response = requests.get(url)
    if response.status_code == 200:
        history = response.json()
        return history
    else:
        return None

def UserRating(username):
    user_info = UserInfo(username)
    if user_info is not None:
        latestRating = user_info[-1]["NewRating"]
        # print(f"Latest Rating: {latestRating}")
        ratedCount = len([participation for participation in user_info if participation["IsRated"]])
        # print(f"Rated Count: {ratedCount}")
        return {latestRating, ratedCount}
    else:
        return {0, 0}

# res = UserRating("ritsuepi")
# print(res)