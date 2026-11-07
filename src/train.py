"""Leave-countries-out evaluation: predict chloroquine resistance WITHOUT the crt locus.

Run:  python src/train.py
"""
import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline

from data import load_pf7
from features import build_features

SEED = 42
N_SPLITS = 5


def gbm():
    return HistGradientBoostingClassifier(random_state=SEED)


def logreg():
    return make_pipeline(SimpleImputer(strategy="most_frequent"),
                         LogisticRegression(max_iter=1000))


def cv_auc(X, y, groups, cols, make_model):
    """Mean and per-fold AUC when whole countries are held out."""
    aucs = []
    for tr, te in GroupKFold(n_splits=N_SPLITS).split(X, y, groups):
        m = make_model().fit(X.iloc[tr][cols], y.iloc[tr])
        p = m.predict_proba(X.iloc[te][cols])[:, 1]
        aucs.append(float(roc_auc_score(y.iloc[te], p)))
    return {"mean_auc": round(sum(aucs) / len(aucs), 3),
            "fold_aucs": [round(a, 3) for a in aucs]}


def main(out="results.json"):
    df = load_pf7()
    X = build_features(df)
    y = df["Chloroquine"].map({"Resistant": 1, "Sensitive": 0})
    keep = y.notna()                       # drop 'Undetermined' labels
    X, y, groups = X[keep], y[keep].astype(int), df.loc[keep, "Country"]
    X = X.assign(Year=df.loc[keep, "Year"])

    # Circular sanity check: crt_76 IS the label rule, so this should be ~1.0
    results = {"n_samples": int(keep.sum()), "n_countries": int(groups.nunique())}
    results["circular_baseline_crt76"] = cv_auc(X, y, groups, ["crt_76[K]"], gbm)

    base = [c for c in X.columns if c not in ("crt_76[K]", "Year")]
    k13 = [c for c in base if c.startswith("k13_")]
    sp = [c for c in base if c.startswith(("dhfr", "dhps"))]
    experiments = {
        "year_only": (["Year"], gbm),
        "all_loci_no_crt": (base, gbm),
        "all_loci_plus_year": (base + ["Year"], gbm),
        "no_kelch13": ([c for c in base if c not in k13], gbm),
        "sp_loci_only": (sp, gbm),
        "no_sp_loci": ([c for c in base if c not in sp], gbm),
        "logistic_all_loci_no_crt": (base, logreg),
    }
    for name, (cols, mk) in experiments.items():
        results[name] = cv_auc(X, y, groups, cols, mk)
        print(f"{name:<28} {results[name]['mean_auc']}")

    Path(out).write_text(json.dumps(results, indent=2))
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
