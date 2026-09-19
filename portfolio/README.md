# Business Analytics Portfolio

Five deployable Streamlit dashboards:

| Project | Entrypoint | Dependencies | Dashboard |
|---|---|---|---|
| RetainIQ | `portfolio/retainiq/app.py` | `portfolio/retainiq/requirements.txt` | SaaS churn + MRR at risk |
| FunnelIQ | `portfolio/funneliq/app.py` | `portfolio/funneliq/requirements.txt` | Attribution + funnel ROI |
| SupplyPulse | `portfolio/supplypulse/app.py` | `portfolio/supplypulse/requirements.txt` | Forecast + reorder risk |
| AttritionRadar | `portfolio/attritionradar/app.py` | `portfolio/attritionradar/requirements.txt` | Workforce attrition + cost |
| Monsoon-to-Margin | `portfolio/monsoon-to-margin/app.py` | `portfolio/monsoon-to-margin/requirements.txt` | Live weather + disruption model |

## Deploy all five with Streamlit Community Cloud

Streamlit Community Cloud can deploy multiple apps from a single GitHub repository. Each app can have its own entrypoint and its own `requirements.txt` beside that entrypoint.

1. Open https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → **Yup, I have an app**.
3. For each row above, choose:
   - Repository: `Harshavardhan-xo/customer-shopping-behavior-analysis`
   - Branch: `main`
   - File path: the listed entrypoint
4. Pick a memorable subdomain such as:
   - `harsha-retainiq`
   - `harsha-funneliq`
   - `harsha-supplypulse`
   - `harsha-attritionradar`
   - `harsha-monsoon-margin`
5. Click **Deploy**.

Once deployed, each app gets its own public `streamlit.app` URL. Code changes pushed to GitHub are automatically reflected in the deployed app, and dependency changes trigger a redeploy.

## Important

The dashboards use synthetic data unless explicitly stated otherwise. Monsoon-to-Margin pulls weather data from Open-Meteo when available and uses a documented simulated quick-commerce disruption layer for orders, cancellations, rider availability, revenue, and costs.

Existing repository content outside `portfolio/` is preserved.
