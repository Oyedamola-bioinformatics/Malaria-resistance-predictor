"""Download and merge the MalariaGEN Pf7 tables (Zenodo record 18711720)."""
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

ZENODO = "https://zenodo.org/records/18711720/files"
FILES = {
    "samples": "Pf7_samples.txt",
    "genotypes": "Pf7_drug_resistance_marker_genotypes.txt",
    "resistance": "Pf7_inferred_resistance_status_classification.txt",
}


def download(data_dir="data"):
    """Fetch any missing Pf7 file into data_dir (never committed to git)."""
    d = Path(data_dir)
    d.mkdir(exist_ok=True)
    for name in FILES.values():
        path = d / name
        if not path.exists() or path.stat().st_size == 0:
            print(f"Downloading {name} ...")
            urlretrieve(f"{ZENODO}/{name}?download=1", path)
    return d


def load_pf7(data_dir="data"):
    """Return one table: metadata + genotypes + inferred resistance (16,203 QC-pass samples)."""
    d = download(data_dir)
    meta = pd.read_csv(d / FILES["samples"], sep="\t")
    geno = pd.read_csv(d / FILES["genotypes"], sep="\t")
    res = pd.read_csv(d / FILES["resistance"], sep="\t")
    geno = geno.rename(columns={"Unnamed: 0": "Sample"})
    return meta.merge(geno, on="Sample").merge(res, on="Sample")
