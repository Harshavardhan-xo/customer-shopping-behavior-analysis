from pathlib import Path
import sqlite3,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DB=ROOT/"attritionradar.db"

def load(path=DB):
    if not path.exists():
        raise FileNotFoundError("Run data/generate_synthetic_data.py first.")
    q="""SELECT e.*,CASE WHEN x.employee_id IS NULL THEN 0 ELSE 1 END exited,
    CASE WHEN x.exit_reason='voluntary' THEN 1 ELSE 0 END voluntary_exit,
    COALESCE(x.is_regretted,0) is_regretted
    FROM employees e LEFT JOIN exits x USING(employee_id);"""
    with sqlite3.connect(path) as c:
        return pd.read_sql_query(q,c)

def turnover(path=DB):
    q=ROOT/"queries/turnover_rates.sql"
    with sqlite3.connect(path) as c:
        return pd.read_sql_query(q.read_text(),c)