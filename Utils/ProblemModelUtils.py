import math
from typing import Optional
from Model.ProblemModel import ProblemModel, ProblemModelWithDifficultyModel, ProblemModelWithTimeModel

def predict_solve_probability(problem_model: ProblemModelWithDifficultyModel, internal_rating: float) -> float:
    """
    ユーザーの内部評価に基づいて、問題を解く確率を予測します。
    
    :param problem_model: ProblemModelWithDifficultyModel, 問題の難易度モデル（discrimination と raw_difficulty を含む）
    :param internal_rating: float, ユーザーの内部レート
    :return: float, 問題を解く確率
    """
    return 1 / (1 + math.exp(-problem_model.discrimination * (internal_rating - problem_model.raw_difficulty)))


def predict_solve_time(problem_model: ProblemModelWithTimeModel, internal_rating: float) -> float:
    """
    ユーザーの内部評価に基づいて、問題を解く時間を予測します。
    
    :param problem_model: ProblemModelWithTimeModel, 問題の時間モデル（slope と intercept を含む）
    :param internal_rating: float, ユーザーの内部レート
    :return: float, 解決にかかる予測時間（秒単位）
    """
    log_time = problem_model.slope * internal_rating + problem_model.intercept
    return math.exp(log_time)


def calculate_top_player_equivalent_effort(problem_model: ProblemModelWithTimeModel) -> float:
    """
    トッププレイヤー（評価: 4000）の努力（解決時間）を計算します。
    
    :param problem_model: ProblemModelWithTimeModel, 問題の時間モデル
    :return: float, トッププレイヤーの解決時間（秒単位）
    """
    top_player_rating = 4000
    return predict_solve_time(problem_model, top_player_rating)


def format_predicted_solve_time(predicted_solve_time: Optional[float]) -> str:
    """
    予測された解決時間を、ユーザーが理解しやすい形式にフォーマットします。
    
    :param predicted_solve_time: float, 予測された解決時間（秒単位）。None の場合もあり得る。
    :return: str, フォーマットされた解決時間
    """
    if predicted_solve_time is None:
        return "-"
    elif predicted_solve_time < 30:
        return "<1 min"
    else:
        minutes = round(predicted_solve_time / 60)
        if minutes > 1:
            return f"{minutes} mins"
        else:
            return f"{minutes} min"


def format_predicted_solve_probability(predicted_solve_probability: Optional[float]) -> str:
    """
    予測された解決確率を、ユーザーが理解しやすい形式にフォーマットします。
    
    :param predicted_solve_probability: float, 予測された解決確率。None の場合もあり得る。
    :return: str, フォーマットされた解決確率
    """
    if predicted_solve_probability is None:
        return "-"
    elif predicted_solve_probability < 0.005:
        return "<1%"
    elif predicted_solve_probability > 0.995:
        return ">99%"
    else:
        percents = round(predicted_solve_probability * 100)
        return f"{percents}%"