import requests
import json

def get_submissions(username, timestamp):

    submissions_url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={timestamp}"
    submissions_response = requests.get(submissions_url)
    if submissions_response.status_code == 200:
        submissions = submissions_response.json()
        return submissions
    else:
        return None