import pandas as pd
from src.simulate_orders import simulate

def make(rain):
    return pd.DataFrame({"date":pd.date_range("2026-01-01",periods=1),"rainfall_mm":[rain],
                         "temp_max_c":[30],"temp_min_c":[24]})

def test_monotonicity():
    dry=simulate(make(1)).iloc[0]; heavy=simulate(make(80)).iloc[0]
    assert heavy.orders>=dry.orders
    assert heavy.avg_delivery_min>=dry.avg_delivery_min
    assert heavy.cancellation_rate>=dry.cancellation_rate
    assert heavy.rider_availability_pct<=dry.rider_availability_pct

def test_empty():
    df=pd.DataFrame(columns=["date","rainfall_mm","temp_max_c","temp_min_c"])
    assert simulate(df).empty