import requests
import json

def get_problem_models():
    # 問題モデルのURL
    problem_models_url = "https://kenkoooo.com/atcoder/resources/problem-models.json"

    # HTTPリクエストを送信
    response = requests.get(problem_models_url)

    # レスポンスのステータスコードをチェック
    if response.status_code == 200:
        # JSONデータを取得
        problem_models = response.json()
        return problem_models
    else:
        return None