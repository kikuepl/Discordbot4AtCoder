from Model.ProblemModel import (
    ProblemModel,
    ProblemModelWithDifficultyModel,
    ProblemModelWithTimeModel,
)
from Utils.ProblemModelUtils import (
    predict_solve_probability,
    predict_solve_time,
    calculate_top_player_equivalent_effort,
    format_predicted_solve_time,
    format_predicted_solve_probability,
)
from Utils.get_problem_models import get_problem_models
from Utils.get_submissions import get_submissions
import numbers


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


def to_time_model(src) -> ProblemModelWithTimeModel:
    """
    任意の入力を ProblemModelWithTimeModel に統一する
    必須フィールド: slope / intercept / variance
    """
    if isinstance(src, ProblemModelWithTimeModel):
        return src

    # dict 形式
    if isinstance(src, dict):
        _check_time_dict(src)
        return ProblemModelWithTimeModel(
            slope=src["slope"],
            intercept=src["intercept"],
            variance=src["variance"],
            difficulty=src.get("difficulty"),
            raw_difficulty=src.get("raw_difficulty"),
            discrimination=src.get("discrimination"),
            is_experimental=src["is_experimental"],
        )

    # 汎用 ProblemModel 形式
    if isinstance(src, ProblemModel):
        if src.variance is None:
            raise ValueError("ProblemModel.variance が None なので TimeModel 化できません")
        return ProblemModelWithTimeModel(
            slope=src.slope,
            intercept=src.intercept,
            variance=src.variance,
            difficulty=src.difficulty,
            raw_difficulty=src.raw_difficulty,
            discrimination=src.discrimination,
            is_experimental=src.is_experimental,
        )

    raise TypeError(f"Unsupported problem model type: {type(src)}")


def _check_time_dict(d: dict) -> None:
    """TimeModel 化に必要なキーがあるか軽く検査"""
    required = ("slope", "intercept", "variance", "is_experimental")
    missing = [k for k in required if k not in d]
    if missing:
        raise KeyError(f"TimeModel 変換に必要なキーが不足しています: {missing}")


# ---------------------------- #
#   使い方サンプル
# ---------------------------- #

def main() -> None:
    problem_models = get_problem_models()
    if problem_models is None:
        print("Failed to fetch problem models.")
        return
    print("Problem models fetched successfully.")

    # 例 : abc032_c の DifficultyModel
    src = problem_models.get("abc032_c")
    if src is None:
        print("Problem model 'abc032_c' not found.")
        return

    dm = to_difficulty_model(src)
    prob = predict_solve_probability(dm, 1545)
    print(f"[difficulty] internal_rating=1545 → solve_prob={prob:.6f}")

    # 例 : abc032_c の TimeModel
    try:
        tm = to_time_model(src)
    except (KeyError, ValueError, TypeError) as e:
        print(f"TimeModel 変換失敗: {e}")
        return

    sec = predict_solve_time(tm, 1545)
    print(f"[time] internal_rating=1545 → solve_time={sec:.2f} 秒")


if __name__ == "__main__":
    main()
