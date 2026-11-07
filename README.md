# Malaria-resistance-predictor
![CI](https://github.com/Oyedamola-bioinformatics/Malaria-resistance-predictor/actions/workflows/ci.yml/badge.svg)

ML model predicting *P. falciparum* drug resistance from genomic markers.
> **Research use only.** Not a diagnostic or clinical decision tool.
## Question
Can chloroquine resistance be predicted in **countries the model has never
seen**, without using the pfcrt locus that defines the label?

## Data

MalariaGEN Pf7 (MalariaGEN et al., Wellcome Open Research 2023, 8:22,
doi:10.12688/wellcomeopenres.18681.1), 16,203 QC-pass samples from 33
countries, downloaded from Zenodo (record 18711720) by `src/data.py`.

## Important: label circularity

Pf7's inferred resistance labels are derived from the genotype columns by
fixed rules. For chloroquine, `crt_76` maps directly onto the label: a model
given that column scores AUC 1.0 in every fold (see table). That result says
nothing about biology, so the headline experiment excludes `crt_76`.

## Method

- Features: binary mutant/wild-type flags for dhfr, dhps, kelch13 and pm2
  duplication (`src/features.py`). Mixed and failed calls are kept as missing.
- Target: chloroquine Resistant vs Sensitive (1,034 Undetermined samples
  dropped; 15,169 used).
- Validation: 5-fold GroupKFold, **whole countries held out** per fold.
- Models: HistGradientBoosting (main), logistic regression (comparison).

## Results (mean AUC on held-out countries)

| Features | Model | Mean AUC |
|---|---|---|
| crt_76 only (circular check) | GBM | 1.000 |
| Year only | GBM | 0.436 |
| All loci, no crt | GBM | 0.726 |
| All loci + Year | GBM | 0.704 |
| No kelch13 | GBM | 0.715 |
| SP loci (dhfr/dhps) only | GBM | 0.704 |
| No SP loci | GBM | 0.624 |
| All loci, no crt | Logistic | 0.687 |

Per-fold values are in `results.json`.

**Interpretation.** The dhfr/dhps (sulfadoxine-pyrimethamine) loci carry most
of the signal: they alone reach 0.704, and removing them drops the score to
0.624. This is consistent with shared drug-use history across regions, but it
is correlational. Year alone is worse than chance, so the signal is not a
simple time trend.

## Limitations

- Fold scores range widely (about 0.5 to 0.87) and each fold holds out only
  3-8 countries, so differences under ~0.03 between rows are not reliable.
- Labels are rule-derived from genotypes, not measured phenotypes.
- About 1% of artemisinin-resistant samples carry rare kelch13 variants not
  in the marker list.
- Mixed-infection calls are treated as missing.
- Artemisinin resistance is concentrated in Southeast Asia, so a
  held-out-country test is not meaningful for it.

## Reproduce

    pip install -r requirements.txt
    python src/train.py      # downloads data, writes results.json
    pytest
    "Verified from a clean clone: results match the table above exactly (seed 42)."

## License

MIT

![CI](https://github.com/Oyedamola-bioinformatics/Malaria-resistance-predictor/actions/workflows/ci.yml/badge.svg)
