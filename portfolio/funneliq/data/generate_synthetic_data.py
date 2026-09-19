import sqlite3,numpy as np,pandas as pd
from pathlib import Path
DB=Path(__file__).resolve().parents[1]/"funneliq.db"
CHANNELS=["paid_social","search","email","referral","organic"]; COST={"paid_social":4,"search":7,"email":.8,"referral":1.2,"organic":.2}

def init_db(n=5000,seed=42):
    r=np.random.default_rng(seed); start=pd.Timestamp.today().normalize()-pd.Timedelta(days=89)
    touch=[]; funnel=[]; purchase=[]
    for uid in range(1,n+1):
        k=int(r.integers(1,6)); ch=r.choice(CHANNELS,k,p=[.32,.22,.14,.12,.2]); base=start+pd.Timedelta(days=int(r.integers(0,90))); t=base
        for j,c in enumerate(ch):
            t=t+pd.Timedelta(hours=int(r.integers(1,48))) if j else t
            touch.append([uid,t,c,f"C{int(r.integers(1,21)):03d}",round(COST[c]*r.uniform(.7,1.3),2)])
        s=r.random()<{"paid_social":.48,"search":.6,"email":.66,"referral":.7,"organic":.52}[ch[0]]
        tr=s and r.random()<.63; buy=tr and r.random()<.36
        stages=["visit"]+(['signup'] if s else [])+(['trial'] if tr else [])+(['purchase'] if buy else [])
        for i,stage in enumerate(stages): funnel.append([uid,base+pd.Timedelta(hours=i*6),stage])
        if buy: purchase.append([uid,base.date(),round(r.lognormal(4.2,.45),2)])
    if DB.exists(): DB.unlink()
    with sqlite3.connect(DB) as c:
        pd.DataFrame(touch,columns=["user_id","timestamp","channel","campaign_id","cost_attributed"]).to_sql("touchpoints",c,index=False)
        pd.DataFrame(funnel,columns=["user_id","timestamp","stage"]).to_sql("funnel_events",c,index=False)
        pd.DataFrame(purchase,columns=["user_id","purchase_date","revenue"]).to_sql("purchases",c,index=False)

if __name__=="__main__":
    init_db(); print(DB)