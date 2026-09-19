from pathlib import Path
import sqlite3,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DB=ROOT/"attritionradar.db"
LEVELS=["IC1","IC2","IC3","IC4","IC5","M1","M2","M3"]
DEPTS=["Sales","Support","Engineering","Finance","HR","Operations","Marketing","Product"]
BANDS=["L1","L2","L3","L4","L5","L6","M4","M5","M6","M7"]

def init_db(n=3000,seed=42,path=DB):
    r=np.random.default_rng(seed); ids=np.arange(1,n+1)
    dept=r.choice(DEPTS,n); level=r.choice(LEVELS,n); tenure=r.integers(1,121,n)
    salary=r.choice(BANDS,n); perf=r.integers(1,6,n); promo=np.minimum(tenure,r.integers(0,49,n))
    z=-3+.045*promo+.65*np.isin(dept,["Sales","Support"])+.2*(perf<=2)-.35*(perf>=4)+r.normal(0,.35,n)
    p=1/(1+np.exp(-z)); exited=r.random(n)<p; voluntary=exited&(r.random(n)>.15); regretted=voluntary&(perf>=4)
    end=pd.Timestamp.today().normalize()
    dates=[(end-pd.DateOffset(months=int(r.integers(0,min(24,max(1,t))+1)))).date() if e else None for t,e in zip(tenure,exited)]
    employees=pd.DataFrame({"employee_id":ids,"department":dept,"job_level":level,"tenure_months":tenure,"salary_band":salary,"performance_rating":perf,"last_promotion_months_ago":promo,"manager_id":r.integers(9000,9300,n)})
    exits=pd.DataFrame({"employee_id":ids[exited],"exit_date":np.array(dates,dtype=object)[exited],"exit_reason":np.where(voluntary[exited],"voluntary","involuntary"),"is_regretted":regretted[exited]})
    if path.exists(): path.unlink()
    with sqlite3.connect(path) as c:
        employees.to_sql("employees",c,index=False)
        exits.to_sql("exits",c,index=False)

if __name__=="__main__":
    init_db()
    print(DB)