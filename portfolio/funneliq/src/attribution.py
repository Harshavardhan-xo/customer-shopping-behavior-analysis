import pandas as pd
import sqlite3
from pathlib import Path

DB=Path(__file__).resolve().parents[1]/"funneliq.db"

def _load(path=None):
    path=DB if path is None else path
    with sqlite3.connect(path) as c:
        touches=pd.read_sql_query("SELECT * FROM touchpoints",c)
        purchases=pd.read_sql_query("SELECT * FROM purchases",c)
    return purchases.merge(touches,on="user_id",how="left").sort_values(["user_id","timestamp"])

def _metrics(df):
    df=df.copy()
    df["ROI"]=df.revenue_attributed/df.cost_attributed.replace(0,pd.NA)
    df["CAC"]=df.cost_attributed/df.conversions.replace(0,pd.NA)
    return df

def last_touch(path=None):
    d=_load(path).groupby("user_id",as_index=False).tail(1)
    return _metrics(d.groupby("channel",as_index=False).agg(
        revenue_attributed=("revenue","sum"),cost_attributed=("cost_attributed","sum"),
        conversions=("user_id","nunique")))

def linear(path=None):
    d=_load(path); d["revenue_piece"]=d.revenue/d.groupby("user_id").channel.transform("count")
    return _metrics(d.groupby("channel",as_index=False).agg(
        revenue_attributed=("revenue_piece","sum"),cost_attributed=("cost_attributed","sum"),
        conversions=("user_id","nunique")))

def recommend(df,pct=.10):
    x=df.dropna(subset=["ROI"]).sort_values("ROI"); low=x.iloc[0]; high=x.iloc[-1]
    shift=float(low.cost_attributed*pct)
    return {"from_channel":low.channel,"to_channel":high.channel,
            "estimated_incremental_revenue":max(0,shift*(float(high.ROI)-float(low.ROI)))}