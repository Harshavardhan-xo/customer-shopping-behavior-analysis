import streamlit as st, plotly.express as px
from src.attrition_model import train_and_score
from src.db import load, turnover
from src.cost_model import estimate

st.set_page_config(page_title="AttritionRadar", layout="wide")
st.title("AttritionRadar — Workforce Attrition & Cost")
try:
    scores, auc = train_and_score()
    full = load()
except FileNotFoundError:
    st.error("Run python data/generate_synthetic_data.py first.")
    st.stop()

threshold = st.sidebar.slider("Risk threshold",0.0,1.0,0.5,0.05)
departments = st.sidebar.multiselect("Department", sorted(scores.department.unique()), default=sorted(scores.department.unique()))
risk = scores[(scores.risk_score >= threshold) & scores.department.isin(departments)]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Voluntary Turnover", f"{full.voluntary_exit.mean():.1%}")
c2.metric("Regretted Loss", f"{full.is_regretted.mean():.1%}")
c3.metric("At-Risk", f"{len(risk):,}")
c4.metric("Cost Exposure", f"₹{estimate(risk):,.0f}")

left,right = st.columns(2)
by = turnover().groupby("department", as_index=False).voluntary_turnover_rate.mean()
left.plotly_chart(px.bar(by,x="voluntary_turnover_rate",y="department",orientation="h",title="Turnover by Department"),use_container_width=True)
right.plotly_chart(px.histogram(scores,x="risk_score",nbins=30,title="Risk Distribution"),use_container_width=True)
st.dataframe(risk[["employee_id","department","job_level","risk_score","top_risk_driver"]].sort_values("risk_score",ascending=False),use_container_width=True)
st.caption(f"Logistic AUC {auc['logistic_auc']:.3f} | RF AUC {auc['random_forest_auc']:.3f}")