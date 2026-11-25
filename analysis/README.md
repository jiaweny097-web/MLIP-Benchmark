# Numerical results supporting the final figures

Final artwork is in plots/. This directory contains source rows and metrics,
not older pictures, manuscript editing notes or duplicate releases.

- fig2b: 3,814 task cases and 48 metallic species. Each case contributes once per
  species, not per atom/model. Bulk 3,098, vacancy 100, surface 504, SFE 108,
  tensile 4. No global geometry deduplication across different task cases.
- sfe_nonI1: main 108-pair metrics and common-pair/exclusion information; full
  109-pair sensitivity is numerical evidence of the exclusion effect. SI/Table_S4
  reports total-energy error in eV; the residual energy-difference error is in
  energy_error_cancellation.csv. It is not the separate SI Table S3 static test.
- tensile: Table 3, per-element curve metrics and peak stresses (NequIP nequip1).
- fig7b: updated matrix and explicit SFE metric ranks. SFE uses equal mean ranks
  of MAE/RMSE/MAPE (ascending) and R2 (descending), then score=11-rank. This
  aggregation was not implemented in the original manual matrix. Other seven
  axes retain original authored scores, not independently recomputed scores.

Code regenerates analytical panels; plots/ contains author-composed final layouts.
