import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from .db import load

NUM=["tenure_months","last_promotion_months_ago","performance_rating"]
CAT=["department","job_level","salary_band"]

def train_and_score(path=None,seed=42):
    df=load(path) if path else load()
    X=df[NUM+CAT]; y=df.voluntary_exit
    a,b,ya,yb=train_test_split(X,y,test_size=.2,stratify=y,random_state=seed)
    pre=ColumnTransformer([("n",StandardScaler(),NUM),("c",OneHotEncoder(handle_unknown="ignore"),CAT)])
    lr=Pipeline([("pre",pre),("m",LogisticRegression(max_iter=2000,random_state=seed))])
    rf=Pipeline([("pre",pre),("m",RandomForestClassifier(n_estimators=200,random_state=seed,class_weight="balanced"))])
    lr.fit(a,ya); rf.fit(a,ya)
    auc={"logistic_auc":float(roc_auc_score(yb,lr.predict_proba(b)[:,1])),
         "random_forest_auc":float(roc_auc_score(yb,rf.predict_proba(b)[:,1]))}
    active=df[df.exited==0].copy()
    active["risk_score"]=rf.predict_proba(active[NUM+CAT])[:,1]
    names=rf.named_steps["pre"].get_feature_names_out()
    imp=rf.named_steps["m"].feature_importances_
    active["top_risk_driver"]=names[int(np.argmax(imp))].replace("n__","").replace("c__","")
    return active,auc