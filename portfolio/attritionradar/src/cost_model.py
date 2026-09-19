RATES={"IC1":.5,"IC2":.5,"IC3":.8,"IC4":.8,"IC5":.8,"M1":1.2,"M2":1.2,"M3":1.2}
SALARY={"L1":450000,"L2":600000,"L3":800000,"L4":1000000,"L5":1300000,"L6":1650000,"M4":1600000,"M5":2000000,"M6":2500000,"M7":3200000}

def estimate(df):
    if df.empty:
        return 0.0
    x=df.copy()
    return float((x.job_level.map(RATES).fillna(.8)*x.salary_band.map(SALARY).fillna(800000)).sum())