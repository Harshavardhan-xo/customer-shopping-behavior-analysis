from data.generate_synthetic_data import init_db
from src.attribution import last_touch,linear

def test_revenue_conservation():
    init_db()
    a=last_touch()
    b=linear()
    assert round(a.revenue_attributed.sum(),6)==round(b.revenue_attributed.sum(),6)
    assert a.revenue_attributed.sum()>0