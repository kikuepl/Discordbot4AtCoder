import math
from typing import Optional
import numbers

# ProblemModelの定義
class ProblemModel:
    def __init__(self, slope: Optional[numbers.Number], intercept: Optional[numbers.Number], 
                 difficulty: Optional[numbers.Number], raw_difficulty: Optional[numbers.Number],
                 discrimination: Optional[numbers.Number], is_experimental: bool, 
                 variance: Optional[numbers.Number]):
        self.slope = slope
        self.intercept = intercept
        self.difficulty = difficulty
        self.raw_difficulty = raw_difficulty
        self.discrimination = discrimination
        self.is_experimental = is_experimental
        self.variance = variance


# ProblemModelWithDifficultyModelの定義
class ProblemModelWithDifficultyModel(ProblemModel):
    def __init__(self, slope: numbers.Number, intercept: numbers.Number, difficulty: numbers.Number,
                 raw_difficulty: numbers.Number, discrimination: numbers.Number, is_experimental: bool):
        super().__init__(slope, intercept, difficulty, raw_difficulty, discrimination, is_experimental, None)
        self.difficulty = difficulty
        self.raw_difficulty = raw_difficulty
        self.discrimination = discrimination


# ProblemModelWithTimeModelの定義
class ProblemModelWithTimeModel(ProblemModel):
    def __init__(self, slope: numbers.Number, intercept: numbers.Number, variance: numbers.Number,
                 difficulty: Optional[numbers.Number], raw_difficulty: Optional[numbers.Number],
                 discrimination: Optional[numbers.Number], is_experimental: bool):
        super().__init__(slope, intercept, difficulty, raw_difficulty, discrimination, is_experimental, variance)
        self.variance = variance


# 型チェック関数
def is_problem_model(obj: object) -> bool:
    return isinstance(obj, ProblemModel) and \
           isinstance(obj.slope, numbers.Number) and \
           isinstance(obj.intercept, numbers.Number) and \
           isinstance(obj.difficulty, numbers.Number) and \
           isinstance(obj.raw_difficulty, numbers.Number) and \
           isinstance(obj.discrimination, numbers.Number) and \
           isinstance(obj.is_experimental, bool) and \
           isinstance(obj.variance, numbers.Number)


def is_problem_model_with_difficulty_model(obj: object) -> bool:
    return isinstance(obj, ProblemModelWithDifficultyModel) and \
           isinstance(obj.slope, numbers.Number) and \
           isinstance(obj.intercept, numbers.Number) and \
           isinstance(obj.difficulty, numbers.Number) and \
           isinstance(obj.raw_difficulty, numbers.Number) and \
           isinstance(obj.discrimination, numbers.Number) and \
           isinstance(obj.is_experimental, bool)


def is_problem_model_with_time_model(obj: object) -> bool:
    return isinstance(obj, ProblemModelWithTimeModel) and \
           isinstance(obj.slope, numbers.Number) and \
           isinstance(obj.intercept, numbers.Number) and \
           isinstance(obj.variance, numbers.Number) and \
           (isinstance(obj.difficulty, numbers.Number) or obj.difficulty is None) and \
           (isinstance(obj.raw_difficulty, numbers.Number) or obj.raw_difficulty is None) and \
           (isinstance(obj.discrimination, numbers.Number) or obj.discrimination is None) and \
           isinstance(obj.is_experimental, bool)


# JSONデータ例
# problem_data = {
#     "abc138_a": {
#         "slope": -0.0007168608759555057,
#         "intercept": 5.865100960838195,
#         "variance": 0.926552668651041,
#         "difficulty": -848,
#         "discrimination": 0.004479398673070138,
#         "irt_loglikelihood": -260.5412324380486,
#         "irt_users": 4554,
#         "is_experimental": False
#     }
# }

# 問題データをProblemModelに変換
# problem = problem_data["abc138_a"]

# # 必要なデータが存在する場合にのみ、問題モデルを作成するように修正
# problem_model = ProblemModel(
#     slope=problem.get("slope"),
#     intercept=problem.get("intercept"),
#     difficulty=problem.get("difficulty"),
#     raw_difficulty=problem.get("difficulty"),  # rawDifficultyもdifficultyと同じとして扱う
#     discrimination=problem.get("discrimination"),
#     is_experimental=problem.get("is_experimental"),
#     variance=problem.get("variance")
# )

# print("slope type:", type(problem_model.slope))
# print("intercept type:", type(problem_model.intercept))
# print("difficulty type:", type(problem_model.difficulty))
# print("raw_difficulty type:", type(problem_model.raw_difficulty))
# print("discrimination type:", type(problem_model.discrimination))
# print("is_experimental type:", type(problem_model.is_experimental))
# print("variance type:", type(problem_model.variance))

# # 型チェック
# if is_problem_model(problem_model):
#     print("This is a valid ProblemModel.")
# else:
#     print("This is NOT a valid ProblemModel.")

# if is_problem_model_with_difficulty_model(problem_model):
#     print("This is a valid ProblemModelWithDifficultyModel.")
# else:
#     print("This is NOT a valid ProblemModelWithDifficultyModel.")

# if is_problem_model_with_time_model(problem_model):
#     print("This is a valid ProblemModelWithTimeModel.")
# else:
#     print("This is NOT a valid ProblemModelWithTimeModel.")
