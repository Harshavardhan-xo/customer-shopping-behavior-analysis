from data.generate_synthetic_data import init_db
from src.churn_model import train_and_score

def test_scores_in_range(tmp_path):
    db = tmp_path / "r.db"
    init_db(db)
    scored, auc = train_and_score(db)
    assert scored.risk_score.between(0,1).all()
    assert auc >= 0