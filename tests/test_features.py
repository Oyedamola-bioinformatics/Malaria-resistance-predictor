import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from features import mutant_flag, build_features  # noqa: E402


def test_mutant_flag_basic():
    s = pd.Series(["K", "T", "T,K", "-", "K,T"])
    out = mutant_flag(s, "K")
    assert out.iloc[0] == 0.0          # wild type
    assert out.iloc[1] == 1.0          # mutant
    assert np.isnan(out.iloc[2])       # mixed call
    assert np.isnan(out.iloc[3])       # failed call
    assert np.isnan(out.iloc[4])       # mixed call


def test_kelch13_wildtype_vs_failed():
    df = pd.DataFrame({
        "crt_76[K]": ["K"] * 3, "dhfr_51[N]": ["N"] * 3, "dhfr_59[C]": ["C"] * 3,
        "dhfr_108[S]": ["S"] * 3, "dhfr_164[I]": ["I"] * 3, "dhps_437[G]": ["A"] * 3,
        "dhps_540[K]": ["K"] * 3, "dhps_581[A]": ["A"] * 3, "dhps_613[A]": ["A"] * 3,
        "pm2_dup_call": [0, 1, -1],
        "kelch13_349-726_ns_changes": [np.nan, "C580Y", "-"],
    })
    X = build_features(df)
    assert X["k13_any"].iloc[0] == 0.0       # blank = wild type
    assert X["k13_any"].iloc[1] == 1.0       # C580Y present
    assert np.isnan(X["k13_any"].iloc[2])    # '-' = failed call
    assert np.isnan(X["pm2_dup"].iloc[2])    # -1 = missing
