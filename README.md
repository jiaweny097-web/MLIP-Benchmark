# MLIP Benchmark

Data and code for **Evaluating Universal Interatomic Potentials for Metallic
Systems: From Elastic Response to Defect Energetics and Ideal Strength**.

Jiawen Yu, Chaohong Guan, Xiaoqing Liu, Yangshuai Wang, Hong Zhu and Xiaoqin Zeng.

## Contents

- `data/`: extracted references, structures, predictions and supporting tables
  (`figure_sources/`).
- `plots/`: final main and supplementary figures (JPG).
- `code/`: input export, metric calculation and plotting scripts.
- `notebooks/`: six model calculation workflows and shared code.
- `envs-setting/`: Conda environments; `metadata/`: versions, hashes and provenance.

The local `model/` directory is Git-ignored and excluded from the upload ZIP.

## Scope

Bulk: 3,098 structures; vacancy: 100 pairs; surface: 504 slabs; efficiency:
100 inputs; tensile: Al, Cu, Mo and W (NequIP uses nequip1).
SFE excludes I1 and Po: 109 matched model pairs are retained, with 108 used in
the main analysis after excluding MgCa I2. See `data/sfe_nonI1/` for flags and
exclusions. Figure 2b covers 48 metallic species.

## Run

```bash
pip install -r requirements-analysis.txt
python data/verify_data.py
python code/export_inputs.py --output inputs
python code/reproduce_paper.py --task all --output results/paper_reproduction
python code/plot_fig2b_coverage.py
python code/plot_fig5c_nonI1.py
python code/plot_tensile_combined.py
python code/update_SI_radar.py
python code/reproduce_static_metrics.py
```

Input export creates real task CSVs and deduplicated structures from the PKLs.
Use these CSVs with the notebooks and model-specific environments for new
inference. Output goes to `results/`, leaving final `plots/` unchanged.
DFT settings are described in the manuscript/SI.

Some original Fig. 3/SI static metrics remain unresolved; see
`data/figure_sources/static/README.md`. Fig. 7b recalculates SFE only; other
axes retain original authored scores. Bulk-model relaxed coordinates were not
saved. These scripts do not claim exact reproduction of every historical
trajectory or manually composed figure.

## Citation and permissions

Please cite the associated article and the exact repository commit/release:
https://github.com/jiaweny097-web/MLIP-Benchmark

Original code is available for noncommercial research/education; original
data/documentation use CC BY-NC 4.0. Third-party terms remain applicable.
See `LICENSE` for complete terms and source attributions.
