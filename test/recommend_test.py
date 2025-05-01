import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))   # ACbot までを追加

from Model.ProblemModel import (
    ProblemModel,
    ProblemModelWithDifficultyModel,
    ProblemModelWithTimeModel,
)
from Utils.ProblemModelUtils import predict_solve_probability
from Utils.get_problem_models import get_problem_models
from Utils.get_UserInfo import UserRating


# ---------------------------- #
#   変換ヘルパー
# ---------------------------- #

def to_difficulty_model(src) -> ProblemModelWithDifficultyModel:
    """任意の入力を ProblemModelWithDifficultyModel に統一する"""
    if isinstance(src, ProblemModelWithDifficultyModel):
        return src

    if isinstance(src, dict):
        return ProblemModelWithDifficultyModel(
            slope=src["slope"],
            intercept=src["intercept"],
            difficulty=src["difficulty"],
            raw_difficulty=src.get("raw_difficulty", src["difficulty"]),
            discrimination=src["discrimination"],
            is_experimental=src["is_experimental"],
        )

    if isinstance(src, ProblemModel):
        return ProblemModelWithDifficultyModel(
            slope=src.slope,
            intercept=src.intercept,
            difficulty=src.difficulty,
            raw_difficulty=src.raw_difficulty,
            discrimination=src.discrimination,
            is_experimental=src.is_experimental,
        )

    raise TypeError(f"Unsupported problem model type: {type(src)}")


# ---------------------------- #
#   前処理：dict → [(problem_id, model), …]
# ---------------------------- #
def to_model_list(problem_models: dict) -> list[tuple[str, ProblemModelWithDifficultyModel]]:
    res = []
    for pid, value in problem_models.items():
        # 必須パラメータがそろっているものだけ対象にする
        if all(k in value for k in ("slope", "intercept", "difficulty", "discrimination", "is_experimental")):
            try:
                dm = to_difficulty_model(value)
            except Exception as e:        # 変換に失敗したらスキップ
                print(f"[warn] {pid}: {e}")
                continue
            res.append((pid, dm))
    return res


# ---------------------------- #
#   メインロジック
# ---------------------------- #
def main() -> None:
    username = input("ユーザ名を入力してください: ").strip()
    if not username:
        print("ユーザ名が空です。")
        return

    # 1) ユーザの内部レーティング取得
    rate, *_ = UserRating(username)      # UserRating が (rating, …) を返す前提
    print(f"ユーザ {username} のレーティング: {rate}")

    # 2) 問題モデル取得 → list 化
    problem_models = get_problem_models()
    if problem_models is None:
        print("問題モデルの取得に失敗しました。")
        return

    model_list = to_model_list(problem_models)

    # 3) solve 確率を計算してフィルタリング
    recommends = []
    for pid, model in model_list:
        prob = predict_solve_probability(model, rate)   # 0–1
        prob_pct = prob * 100                           # 百分率に換算
        if 45 <= prob_pct <= 55:
            recommends.append((pid, prob_pct))

    # 4) 結果表示
    if not recommends:
        print("該当する問題が見つかりませんでした。")
        return

    # 0.5 に近い順（≒難易度がちょうど良い順）に並べ替え
    recommends.sort(key=lambda x: abs(50 - x[1]))

    print(f"\n★★★ あなたにおすすめの問題 (成功確率 45–55%) は{len(recommends)}個あります★★★")
    # 先頭10個を表示
    for pid, p in recommends[:10]:
        print(f"{pid:15s}  推定成功確率: {p:.1f}%")
    # for pid, p in recommends:
    #     print(f"{pid:15s}  推定成功確率: {p:.1f}%")

    print("--------------------------------------------------")


if __name__ == "__main__":
    main()
