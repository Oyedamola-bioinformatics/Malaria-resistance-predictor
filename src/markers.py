# Resistance markers used in this project, keyed by the feature names that
# src/features.py produces from the MalariaGEN Pf7 genotype table.
#
# Sources: WHO list of artemisinin partial-resistance markers (check the
# current WHO page, as it is updated over time); WWARN molecular surveyor;
# MalariaGEN Pf7 paper (Wellcome Open Research 2023, 8:22) and its
# genotype-to-resistance rules document.

MARKERS = {
    # kelch13 - artemisinin partial resistance.
    # Source: WHO validated/candidate kelch13 marker list. Validation status
    # differs between mutations; rarer ones are candidates or associated only.
    "k13_F446I": "artemisinin",
    "k13_N458Y": "artemisinin",
    "k13_C469Y": "artemisinin",
    "k13_M476I": "artemisinin",
    "k13_Y493H": "artemisinin",
    "k13_R539T": "artemisinin",
    "k13_I543T": "artemisinin",
    "k13_P553L": "artemisinin",
    "k13_R561H": "artemisinin",
    "k13_C580Y": "artemisinin",
    "k13_P441L": "artemisinin",
    "k13_G449A": "artemisinin",
    "k13_P574L": "artemisinin",
    "k13_G538V": "artemisinin",
    "k13_A675V": "artemisinin",
    "k13_C469F": "artemisinin",
    "k13_P527H": "artemisinin",

    # pfcrt - chloroquine. Excluded from the headline model because the
    # Pf7 label is derived directly from this locus (see README).
    # Source: Pf7 genotype-to-resistance rules.
    "crt_76[K]": "chloroquine",

    # dhfr - pyrimethamine (SP).
    # Source: WWARN molecular surveyor; Pf7 rules.
    "dhfr_51[N]": "sp",
    "dhfr_59[C]": "sp",
    "dhfr_108[S]": "sp",
    "dhfr_164[I]": "sp",

    # dhps - sulfadoxine (SP).
    # Source: WWARN molecular surveyor; Pf7 rules.
    "dhps_437[G]": "sp",
    "dhps_540[K]": "sp",
    "dhps_581[A]": "sp",
    "dhps_613[A]": "sp",

    # plasmepsin 2 duplication - piperaquine.
    # Source: Pf7 genotype-to-resistance rules.
    "pm2_dup": "piperaquine",
}
