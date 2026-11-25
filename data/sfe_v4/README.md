# Active SFE database — I1 and Po excluded

The active database omits all I1 and Po-containing records. The author's
unfiltered original files and a recoverable curation backup remain outside the
upload repository. This directory retains110 non-I1/non-Po DFT pairs from the
v4 fault and v2 perfect summaries. One pair (ZnTi I2) has no complete verified
six-model match;109 pairs are common to all six models.

The labelled108-pair analysis additionally applies the author's earlier MgCa I2
exclusion. Its flagged DFT value is retained in the full109-pair data. No other
outlier exclusion is introduced. MgY I2's positive component energies are flagged.

See ../sfe_nonI1/README.md for pairing, exact scopes and source-block resolution.
DFT equation: (E_fault-E_perfect)/|a1 cross a2|*16021.76634 mJ/m2. Energies
are copied from the author-supplied summary Energy columns. Input POSCARs are
provided; local old CONTCARs are not presented as outputs of the new DFT rerun.
No convergence certification or new model inference is asserted.
Recompute DFT values with `python data/sfe_v4/recompute.py` from repository root.
