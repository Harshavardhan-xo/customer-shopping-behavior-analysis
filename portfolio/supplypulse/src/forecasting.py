import math
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

Z={.90:1.2816,.95:1.6449,.99:2.3263}

def forecast_sku(series):
    s=series.astype(float).fillna(0)
    if len(s)<5 or s.sum()==0: return 0.0,float(s.tail(30).std(ddof=0) if len(s) else 0)
    model=SimpleExpSmoothing(s,initialization_method="estimated").fit(optimized=True)
    return max(float(model.forecast(1).iloc[0]),0.0),float(s.tail(30).std(ddof=0))

def reorder_point(forecast,std,lead,service=.95):
    z=Z[min(Z,key=lambda x:abs(x-service))]
    return float(forecast*lead+z*std*math.sqrt(max(lead,0)))