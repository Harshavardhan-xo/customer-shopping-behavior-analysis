import sqlite3,numpy as np,pandas as pd
from pathlib import Path
DB=Path(__file__).resolve().parents[1]/"supplypulse.db"
CATS=["Grocery","Beauty","Home","Electronics","Fashion","Pet"]

def init_db(n=150,days=365,seed=42):
    r=np.random.default_rng(seed); dates=pd.date_range(end=pd.Timestamp.today().normalize(),periods=days)
    skus=[]; sales=[]; inv=[]
    for i in range(1,n+1):
        sku=f"SKU{i:04d}"; cat=r.choice(CATS); cost=float(r.uniform(40,1200)); price=round(cost*r.uniform(1.25,2.3),2); lead=int(r.integers(2,18))
        skus.append([sku,cat,round(cost,2),price,lead]); base=r.uniform(2,35); seasonal=1+.25*np.sin(np.linspace(0,2*np.pi,days)+r.random()*6.2); demand=np.maximum(0,r.poisson(np.maximum(base*seasonal,.1))); on=int(max(5,base*lead*3))
        for dt,u in zip(dates,demand):
            sales.append([sku,dt.date(),int(u)]); on-=int(u)
            if on<int(base*lead): on+=int(base*lead*r.uniform(2,4))
            inv.append([sku,dt.date(),max(on,0)])
    if DB.exists(): DB.unlink()
    with sqlite3.connect(DB) as c:
        pd.DataFrame(skus,columns=["sku_id","category","unit_cost","unit_price","lead_time_days"]).to_sql("skus",c,index=False)
        pd.DataFrame(sales,columns=["sku_id","date","units_sold"]).to_sql("daily_sales",c,index=False)
        pd.DataFrame(inv,columns=["sku_id","date","units_on_hand"]).to_sql("inventory_snapshots",c,index=False)

if __name__=="__main__": init_db(); print(DB)