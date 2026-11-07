# Resistance markers used in this project, keyed by the feature names that
# src/features.py produces from the MalariaGEN Pf7 genotype table.
# Add a source (WHO report / WWARN / paper) next to each group before release.

MARKERS = {
    # kelch13 - artemisinin partial resistance
    # Validated (WHO): F446I, N458Y, C469Y, Y493H, R539T, I543T, P553L,
    # R561H, C580Y, P574L, A675V. Others are candidate/associated: verify status.(WHO report, WWARN)
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

    # pfcrt - chloroquine (excluded from the headline model to avoid circularity)(WHO report, WWARN)
    "crt_76[K]": "chloroquine",

    # dhfr - pyrimethamine (SP)(WHO report, WWARN)
    "dhfr_51[N]": "sp",
    "dhfr_59[C]": "sp",
    "dhfr_108[S]": "sp",
    "dhfr_164[I]": "sp",

    # dhps - sulfadoxine (SP)(WHO report, WWARN)
    "dhps_437[G]": "sp",
    "dhps_540[K]": "sp",
    "dhps_581[A]": "sp",
    "dhps_613[A]": "sp",

    # plasmepsin 2 duplication - piperaquine. (WHO report, WWARN)
    "pm2_dup": "piperaquine",
}
