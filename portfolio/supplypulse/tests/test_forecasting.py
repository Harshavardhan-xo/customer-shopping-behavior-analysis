from src.forecasting import reorder_point

def test_lead_time():
    assert reorder_point(10,2,6) > reorder_point(10,2,3)

def test_variability():
    assert reorder_point(10,1,5) < reorder_point(10,4,5)

def test_zero():
    assert reorder_point(0,0,5)==0