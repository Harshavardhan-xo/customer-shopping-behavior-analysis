from data.generate_synthetic_data import init_db
from src.attrition_model import train_and_score

def test_risk(tmp_path):
    db=tmp_path/"a.db"
    init_db(path=db)
    scored,auc=train_and_score(db)
    assert scored.risk_score.between(0,1).all()
    assert auc["random_forest_auc"]>=0