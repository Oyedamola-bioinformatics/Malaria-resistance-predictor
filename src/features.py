import pandas as pd

# Wild-type alleles; check against the Pf7 rules document
WT = {"crt_76[K]": "K", "dhfr_51[N]": "N", "dhfr_59[C]": "C",
      "dhfr_108[S]": "S", "dhfr_164[I]": "I", "dhps_437[G]": "A",
      "dhps_540[K]": "K", "dhps_581[A]": "A", "dhps_613[A]": "A"}

VALIDATED = ["F446I", "N458Y", "C469Y", "M476I", "Y493H",
             "R539T", "I543T", "P553L", "R561H", "C580Y"]
KELCH13_MARKS = list(dict.fromkeys(
    VALIDATED + ["P441L", "G449A", "P574L", "G538V", "A675V", "C469F", "P527H"]))


def mutant_flag(s, wt):
    """0 = wild type, 1 = single mutant allele, NaN = missing or mixed."""
    s = s.astype(str).str.upper()
    out = pd.Series(float("nan"), index=s.index)
    out[s == wt] = 0.0
    clean = ~s.isin([wt, "-", "NAN"]) & ~s.str.contains(",")
    out[clean] = 1.0
    return out


def build_features(df):
    """df = merged table with the Pf7 genotype columns. Returns the feature table."""
    X = pd.DataFrame({c: mutant_flag(df[c], wt) for c, wt in WT.items()})
    X["pm2_dup"] = df["pm2_dup_call"].replace(-1, float("nan"))

    k = df["kelch13_349-726_ns_changes"].astype(str).str.upper()
    cols = []
    for m in KELCH13_MARKS:
        X[f"k13_{m}"] = k.str.contains(m, regex=False).astype(float)
        cols.append(f"k13_{m}")
    X["k13_any"] = X[cols].max(axis=1)
    X.loc[k == "-", cols + ["k13_any"]] = float("nan")   # failed calls -> missing
    return X
