# Matched SFE excluding all I1 — 2026-11-25

Scope: FCC Al/Cu ISF and ESF, and HCP Mg/Ti/Zn I2. All I1 data are
excluded from this evaluation. DFT comes from fault-summary_results-new-v4.csv
and perfect-summary_results-v2.csv; see ../sfe_v4 for the complete extraction.
After removing the four Po-containing cases from the active database,110
non-I1/non-Po DFT records remain. ZnTi I2 has no complete verified six-model
input/result match. The common subset is109 pairs.
No missing values are filled and no extra ZnMn I2 fault result is invented.

Faults match constrained input geometry, cell and species. Perfect structures
come from the same-type directory and match the corresponding model input.
Original export TARGET_PATHS in benchmark-dft/SFE/sfe.ipynb lists Al isf_match
before esf_match. Archived perfect inputs have 26 Al entries in each block;
duplicated identical inputs with IDs k and k+26 are resolved to the isf or esf
block respectively, not selected by energy. Later summary IDs differ within
these blocks, so newer numerical IDs are not used as model record identifiers.
pairing_audit.csv exposes every candidate and selected raw ID. Saved cells and
fault/perfect atomic compositions are checked. Convergence of archived model
relaxations is not certified by these records.

SFE = (E_fault - E_perfect) / area * 16021.76634 mJ/m2. Area is the full
cross-product norm of the paired perfect in-plane cell vectors. One fault area
is used, consistently with the historical benchmark. Component DFT and model
total energies, area, structures and source identifiers are retained in PKLs.
ID is the stable v4 extraction identifier, not a new contiguous subset number;
pair_key is the physical identity. The same IDs are used by all six models.

Two explicitly labelled plot/metric scopes are supplied:
- all_matched: all 109 common pairs, including the flagged MgCa I2 reference.
- without_MgCa_I2: 108 common pairs, applying the author's previously requested
  MgCa I2 exclusion. This reference gives approximately -45284 mJ/m2; it is
  preserved in full data. Its invalidity has not been established here.
MgY I2 has positive component total energies and remains flagged and included.
No additional exclusion based on prediction errors or ranking is applied.

Reproduce figures and metrics from repository root:
    python code/plot_sfe_nonI1.py

Outputs are in analysis/sfe_nonI1. Each plot has six parity panels with common
axis limits within its scope. MAE/RMSE use mJ/m2. R2 compares squared residuals
to the DFT variance; MAPE excludes only effectively zero DFT values (1e-12).
All model/DFT SFE values are checked against component-energy subtraction.
No model inference or manuscript DOCX edit was performed.

Requested Figure5c composite: `python code/plot_fig5c_nonI1.py` produces
Fig5c_SFE_nonI1_all_matched and Fig5c_SFE_nonI1_without_MgCa_I2 in PNG/SVG/PDF.
The main panel shows ML-minus-DFT errors with boxes; six insets retain the original
Fig5c layout. Metric values are verified against the stored paired-data analysis.
