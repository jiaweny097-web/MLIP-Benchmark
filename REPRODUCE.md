# Reproducing the Available Analyses

This document describes the analyses that can be recomputed from the current
consolidated data release. It does not claim that pending HCP I1 results or the
original global Figure 3 aggregate can already be reproduced.

## Environment setup

Six author-supplied Conda exports are stored in `envs-setting/`. Portable copies
remove only the server-specific environment name and absolute prefix:

```bash
conda env create -f envs-setting/portable/mace-environment.yml
conda activate mlip-mace
```

Repeat with the selected model name. The exports record the actual package sets,
but they do not record the NVIDIA driver or every external pip index used when the
environments were created.

## Verify the released data

```bash
python data/verify_data.py
```

This checks all catalogued PKL envelopes, record counts and hashes, six-model ID coverage,
vacancy formation-energy equations, the 504 surface-energy reconstructions and the
exclusion of I1 from active SFE records.

## Recompute available paper analyses

```bash
python code/reproduce_paper.py --task all --output results/paper_reproduction
```

Individual task choices are `bulk`, `defects`, `tensile`, `efficiency` and
`static`. The command creates CSV metric tables and PNG/SVG figures. Its exact
scope is saved in `results/paper_reproduction/scope.json`.

| Paper content | Command/task | Principal outputs | Scope note |
|---|---|---|---|
| Bulk lattice and elastic indicators | `--task bulk` | `bulk_lattice_elastic_metrics.csv`, `Fig3c_Fig4_available_*.png`, `SI_invalid_elastic_pairs.csv` | Reports both all-finite results and the historical MAPE<=50% filter with sample counts |
| Derived Pugh/Cauchy descriptors | `--task bulk` | `Table2_metallurgical_metrics.csv` | Uses the archived structure classification and explicit valid-pair counts |
| Vacancy and surface panels | `--task defects` | `Fig5ab_vacancy_surface.png`, `Fig5ab_metrics.csv` | SFE has a separate non-I1 entry point: code/plot_fig5c_nonI1.py |
| Ideal tensile curves and Table 3 metrics | `--task tensile` | `Fig6_Mo_sigmaZZ.png`, `Fig6_W_sigmaZZ.png`, `Fig6_Cu_sigmaZZ.png`, `Fig6_Al_sigmaZZ.png` (and SVG), `tensile_peak_values.csv`, `Table3_all_six_metrics.csv` | Four separate figures: Mo/W/Cu use their DFT maximum strains; Al uses the model-test maximum (50%). No legends or model extrapolation. NequIP uses `nequip1`; loading axis z/σzz |
| Relaxation-efficiency/Pareto input | `--task efficiency` | `Fig7a_efficiency.png`, `Fig7_efficiency_pareto.csv` | Recomputes the source arithmetic mean of stored `time_per_step`, including the source zero-step convention |
| Retained static subsets | `--task static` | `static_task_metrics_only.csv` | Bulk and vacancy subsets only; not the original global Figure 3 aggregate |

The extracted numerical functions for tensile metrics are in
`code/reproduce/tensile_original_metrics.py`. Their original notebook/cell and
source hashes are documented in `metadata/reproduction_sources.csv`.

## Rerun model inference

The six model notebooks expose the same eight tasks and call the shared
`notebooks/benchmark_workflows.py`. Checkpoints are selected by environment
variable or the local `model/` path. Actual input manifests must be prepared from
the schemas in `notebooks/config/manifest_examples/`; those example rows are not
the manuscript dataset.

Model files are ignored by Git because checkpoint redistribution and large-file
handling require separate review. Their local SHA-256 values are recorded in
`metadata/models.csv`. Use the exact upstream artifact plus the recorded hash, or
an approved Git LFS/archive strategy.

## DFT settings

DFT settings, convergence criteria and reference definitions are described in the
manuscript and Supporting Information. This repository distributes extracted
structures and numerical results, not licensed VASP binaries/POTCAR or complete
OUTCAR trees. For a final reproducible release, the manuscript/SI must remain the
authoritative settings record and should identify the pseudopotential family and
versions used.

## Pending work

- Align the final manuscript with the current non-I1 release scope; I1 reruns are required only if I1 claims are retained.
- Non-I1 SFE pairs and Figure5c analysis are provided; resolve the flagged references and unmatched ZnTi I2 before claiming broader coverage.
- The tensile loading axis is verified as z/σzz. Existing DOCX files retain their
  previous wording; this repository update does not revise the manuscript.
- Add a tested end-to-end entry point for every final manuscript figure and SI
  table after those data are frozen.
- Create an immutable Git tag/commit and, if used, an archival DOI.


## Updated Figure5c and Figure2b

`python code/plot_fig5c_nonI1.py` uses the matched non-I1 SFE data (109 and labelled108-pair scopes). `python code/plot_fig2b_coverage.py` uses explicit retained source rows, with separate original-source and current-reference populations. See analysis/fig2b/README.md. These are tested local plotting entry points; pending global Figure3 and full manuscript/SI reproduction are not implied.
