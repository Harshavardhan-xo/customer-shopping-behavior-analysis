import pandas as pd
from src.cost_model import estimate

def test_cost_scales():
    row={"job_level":"IC3","salary_band":"L3"}
    one=estimate(pd.DataFrame([row]))
    two=estimate(pd.DataFrame([row,row]))
    assert two==2*one