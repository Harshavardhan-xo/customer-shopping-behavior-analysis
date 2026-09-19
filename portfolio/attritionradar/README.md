# AttritionRadar
### Employee Attrition & Workforce Cost Dashboard

Synthetic workforce analytics using SQLite, SQL turnover views, logistic regression + random forest scoring, and a configurable attrition-cost model.

## Setup
```bash
pip install -r requirements.txt
python data/generate_synthetic_data.py
streamlit run app.py
pytest -q
```

## Cost assumption
Default cost-per-attrition is 50% of annual salary for IC1–IC2, 80% for IC3–IC5, and 120% for M1+. These are configurable assumptions, not guarantees.

## Limitations
Synthetic data only; real HR use requires privacy, governance, calibration, and validation.