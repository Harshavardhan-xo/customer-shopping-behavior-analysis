from datetime import date,timedelta
import logging,numpy as np,pandas as pd,requests
from .config import CITIES,SEED
log=logging.getLogger(__name__)

def fallback(city,start,end):
    r=np.random.default_rng(SEED+abs(hash(city))%1000); ds=pd.date_range(start,end); t=r.normal(29,3,len(ds))
    return pd.DataFrame({"date":ds,"rainfall_mm":np.maximum(0,r.gamma(1.3,15,len(ds))),"temp_max_c":t+3,"temp_min_c":t-3})

def fetch_historical(city,start,end):
    lat,lon=CITIES[city]; p={"latitude":lat,"longitude":lon,"start_date":start.isoformat(),"end_date":end.isoformat(),
       "daily":"precipitation_sum,temperature_2m_max,temperature_2m_min","timezone":"auto"}
    try:
        r=requests.get("https://archive-api.open-meteo.com/v1/archive",params=p,timeout=10); r.raise_for_status()
        d=r.json()["daily"]
        return pd.DataFrame({"date":pd.to_datetime(d["time"]),"rainfall_mm":pd.to_numeric(d["precipitation_sum"]).fillna(0),
                             "temp_max_c":d["temperature_2m_max"],"temp_min_c":d["temperature_2m_min"]})
    except (requests.RequestException,KeyError,TypeError,ValueError) as e:
        log.warning("Weather API failed for %s: %s",city,e); return fallback(city,start,end)

def fetch_current_and_forecast(city):
    return fetch_historical(city,date.today()-timedelta(days=6),date.today()+timedelta(days=7))