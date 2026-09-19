# Monsoon-to-Margin
### Live Quick-Commerce Demand & Disruption Dashboard

Streamlit ops dashboard using live Open-Meteo weather data for seven Indian cities plus a transparent simulated quick-commerce disruption model.

## Live vs simulated
Weather rainfall/temperature are live when the API is reachable. Orders, delivery times, cancellation rate, rider availability, revenue and disruption costs are simulated because real quick-commerce order data is not public.

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
pytest -q
```

Rain bands: none <2.5 mm; light 2.5–15; moderate 15–64.5; heavy 64.5–115.5; very heavy >=115.5 mm/day.

Limitations: the disruption layer is a scenario model, not a causal estimate.