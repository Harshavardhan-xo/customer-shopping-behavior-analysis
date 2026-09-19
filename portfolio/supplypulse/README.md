# SupplyPulse
### Inventory Health & Stockout-Risk Dashboard

Inventory analytics pipeline using synthetic SKU sales, SQL ABC classification, statsmodels exponential smoothing, reorder-point logic, and a Streamlit dashboard.

## Formula
`reorder_point = forecasted_daily_demand * lead_time_days + safety_stock`

`safety_stock = z_score(service_level) * demand_std_dev * sqrt(lead_time_days)`

Default service level: 95%. Overstocks: `days_of_stock > 90`.

## Setup
```bash
pip install -r requirements.txt
python data/generate_synthetic_data.py
streamlit run app.py
pytest -q
```

Limitations: synthetic data, single-echelon inventory model, and no supplier lead-time variability.