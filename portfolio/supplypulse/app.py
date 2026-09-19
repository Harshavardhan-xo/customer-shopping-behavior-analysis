import math,sqlite3,streamlit as st,pandas as pd,plotly.express as px
from pathlib import Path
from src.forecasting import forecast_sku,reorder_point

st.set_page_config(page_title="SupplyPulse",layout="wide")
st.title("SupplyPulse — Inventory Health & Stockout Risk")
DB=Path(__file__).resolve().parent/"supplypulse.db"
try:
    with sqlite3.connect(DB) as c:
        sales=pd.read_sql_query("SELECT * FROM daily_sales",c)
        inv=pd.read_sql_query("SELECT * FROM inventory_snapshots",c)
        skus=pd.read_sql_query("SELECT * FROM skus",c)
except (FileNotFoundError,sqlite3.OperationalError):
    st.error("Run python data/generate_synthetic_data.py first."); st.stop()

cats=st.sidebar.multiselect("Category",sorted(skus.category.unique()),default=sorted(skus.category.unique()))
service=st.sidebar.slider("Service level",.90,.99,.95,.01)
latest=inv.sort_values("date").groupby("sku_id").tail(1)
rows=[]
for x in skus[skus.category.isin(cats)].itertuples():
    ser=sales[sales.sku_id==x.sku_id].sort_values("date").units_sold
    fc,sd=forecast_sku(ser); rp=reorder_point(fc,sd,x.lead_time_days,service)
    on=float(latest.loc[latest.sku_id==x.sku_id,"units_on_hand"].iloc[0])
    days=on/fc if fc else 0
    rows.append({"sku_id":x.sku_id,"category":x.category,"days_of_stock":days,
                 "reorder_point":rp,"suggested_order_qty":max(0,math.ceil(rp-on)),
                 "below_reorder":on<rp,"overstock":days>90,
                 "overstock_value":max(days-90,0)*fc*x.unit_cost,
                 "risk_value":max(rp-on,0)*x.unit_price})
r=pd.DataFrame(rows)

c1,c2,c3,c4=st.columns(4)
c1.metric("Below Reorder",int(r.below_reorder.sum()))
c2.metric("Overstock Value",f"₹{r.loc[r.overstock,'overstock_value'].sum():,.0f}")
c3.metric("Stockout Risk",f"₹{r.loc[r.below_reorder,'risk_value'].sum():,.0f}")
c4.metric("SKUs",r.sku_id.nunique())

st.plotly_chart(px.bar(r.groupby("category",as_index=False).overstock_value.sum(),x="category",y="overstock_value",title="Overstock Value by Category"),use_container_width=True)
st.subheader("Reorder-Flagged SKUs")
st.dataframe(r[r.below_reorder].sort_values("days_of_stock")[["sku_id","category","days_of_stock","reorder_point","suggested_order_qty"]],use_container_width=True)