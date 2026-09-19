# FunnelIQ
### Marketing Attribution & Funnel ROI Dashboard

Compares last-touch and linear attribution across synthetic multi-touch journeys, with funnel conversion, ROI/CAC, reallocation simulation, and Excel export.

## Setup
```bash
pip install -r requirements.txt
python data/generate_synthetic_data.py
streamlit run app.py
pytest -q
```

Last-touch assigns all purchase revenue to the final pre-purchase channel. Linear splits revenue evenly across all touchpoints. Both models conserve total revenue.

Limitation: the dataset is synthetic and attribution is illustrative rather than causal.