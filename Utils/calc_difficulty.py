import math

def calc_difficulty(submissions, problem_models):
    internal_difficulty = problem_models.get(submissions.get("problem_id"), {}).get("difficulty", 0)
    ret = 0
    if internal_difficulty <= 400:
        difficulty_gap = 400 - internal_difficulty
        normalized_gap = difficulty_gap / 400 
        exponential_factor = math.exp(normalized_gap)
        ret = int(400 / exponential_factor) 
    else:
        ret = internal_difficulty
    return ret