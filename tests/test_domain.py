from app import domain, scoring


def test_existing_scoring_model_imports_remain_compatible():
    assert scoring.Vacancy is domain.Vacancy
    assert scoring.CandidateProfile is domain.CandidateProfile
    assert scoring.ScoreResult is domain.ScoreResult
