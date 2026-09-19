import streamlit as st,plotly.express as px,pandas as pd
from pathlib import Path
from src.attribution import last_touch,linear,recommend

st.set_page_config(page_title="FunnelIQ",layout="wide")
st.title("FunnelIQ — Attribution & Funnel ROI")
model=st.sidebar.radio("Attribution model",["last-touch","linear"])
pct=st.sidebar.slider("Reallocation %",0.0,.5,.1,.05)

try:
    attr=last_touch() if model=="last-touch" else linear()
    with __import__("sqlite3").connect(Path(__file__).resolve().parent/"funneliq.db") as c:
        funnel=pd.read_sql_query("SELECT * FROM funnel_events",c)
except FileNotFoundError:
    st.error("Run python data/generate_synthetic_data.py first."); st.stop()

c1,c2,c3,c4=st.columns(4)
c1.metric("Spend",f"$${attr.cost_attributed.sum():,.0f}")
c2.metric("Revenue",f"$${attr.revenue_attributed.sum():,.0f}")
c3.metric("Blended ROI",f"{attr.revenue_attributed.sum()/max(attr.cost_attributed.sum(),1):.2f}x")
c4.metric("Conversions",f"{attr.conversions.sum():,}")

st.plotly_chart(px.funnel(funnel.groupby("stage",as_index=False).user_id.nunique(),y="stage",x="user_id",title="Funnel"),use_container_width=True)
st.plotly_chart(px.bar(attr,x="channel",y="ROI",title=f"ROI by Channel — {model}"),use_container_width=True)
rec=recommend(attr,pct)
st.info(f"Illustrative reallocation: move {pct:.0%} from {rec['from_channel']} to {rec['to_channel']}; estimated incremental revenue $${rec['estimated_incremental_revenue']:,.0f}.")

if st.button("Export 1-page summary to Excel"):
    out=Path("exports"); out.mkdir(exist_ok=True)
    with pd.ExcelWriter(out/"funneliq_exec_summary.xlsx",engine="openpyxl") as w:
        attr.to_excel(w,index=False,sheet_name="Channel ROI")
        pd.DataFrame([rec]).to_excel(w,index=False,sheet_name="Recommendation")
    st.success("Excel summary exported.")