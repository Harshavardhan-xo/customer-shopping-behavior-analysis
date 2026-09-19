from datetime import date,timedelta
import streamlit as st,plotly.express as px
from src.config import CITIES
from src.weather import fetch_current_and_forecast,fetch_historical
from src.simulate_orders import simulate

st.set_page_config(page_title="Monsoon-to-Margin",layout="wide")
st.title("Monsoon-to-Margin — Quick-Commerce Disruption")
city=st.sidebar.selectbox("City",list(CITIES))
mode=st.sidebar.radio("Mode",["Live past-7d + forecast","Historical custom range"])

if mode=="Live past-7d + forecast":
    weather=fetch_current_and_forecast(city)
else:
    start=st.sidebar.date_input("Start",date.today()-timedelta(days=30))
    end=st.sidebar.date_input("End",date.today()-timedelta(days=1))
    weather=fetch_historical(city,start,end)

ops=simulate(weather)
c1,c2,c3,c4,c5=st.columns(5)
c1.metric("Orders",f"{ops.orders.sum():,.0f}")
c2.metric("Revenue",f"₹{ops.revenue_inr.sum():,.0f}")
c3.metric("Avg Delivery",f"{ops.avg_delivery_min.mean():.1f} min")
c4.metric("Cancellations",f"{ops.cancellation_rate.mean():.1%}")
c5.metric("Disruption Cost",f"₹{ops.disruption_cost_inr.sum():,.0f}")
if ops.severity.isin(["heavy","very_heavy"]).any(): st.error("Heavy-rain disruption threshold crossed.")

st.plotly_chart(px.line(ops,x="date",y="orders",title="Orders Over Time"),use_container_width=True)
st.plotly_chart(px.scatter(ops,x="rainfall_mm",y="avg_delivery_min",color="severity",title="Rainfall vs Delivery Delay"),use_container_width=True)
st.plotly_chart(px.bar(ops.groupby("severity",as_index=False).cancellation_rate.mean(),x="severity",y="cancellation_rate",title="Cancellation Rate by Severity"),use_container_width=True)
st.plotly_chart(px.bar(ops,x="date",y=["rider_surge_cost_inr","sla_penalty_inr"],title="Disruption Cost Components"),use_container_width=True)
st.dataframe(ops,use_container_width=True)