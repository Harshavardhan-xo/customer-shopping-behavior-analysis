import numpy as np,pandas as pd
from .config import BANDS,D,BASE_ORDERS,BASE_DELIVERY,BASE_CANCEL,AOV,SURGE,SLA,SEED

def severity(x):
    for name,lo,hi in BANDS:
        if lo<=x<hi:return name
    return "very_heavy"

def simulate(weather_df,seed=SEED):
    r=np.random.default_rng(seed); d=weather_df.copy(); d["severity"]=d.rainfall_mm.apply(severity)
    weekday=np.where(pd.to_datetime(d.date).dt.dayofweek>=4,1.1,1.0)
    d["orders"]=np.maximum(0,np.round(BASE_ORDERS*weekday*d.severity.map(lambda x:D[x][0])+r.normal(0,BASE_ORDERS*.04,len(d)))).astype(int)
    d["avg_delivery_min"]=BASE_DELIVERY+d.severity.map(lambda x:D[x][1])+r.normal(0,.8,len(d))
    d["cancellation_rate"]=np.clip(BASE_CANCEL+d.severity.map(lambda x:D[x][2])+r.normal(0,.003,len(d)),0,.95)
    d["rider_availability_pct"]=d.severity.map(lambda x:D[x][3])
    d["revenue_inr"]=d.orders*(1-d.cancellation_rate)*AOV
    missing=d.orders*(1-d.rider_availability_pct)/25
    d["rider_surge_cost_inr"]=missing*SURGE
    d["sla_penalty_inr"]=d.orders*d.cancellation_rate*SLA
    d["disruption_cost_inr"]=d.rider_surge_cost_inr+d.sla_penalty_inr
    return d