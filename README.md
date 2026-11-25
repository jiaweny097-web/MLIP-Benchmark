# MLIP Benchmark

Data, model predictions and analysis code supporting **Evaluating Universal
Interatomic Potentials for Metallic Systems: From Elastic Response to Defect
Energetics and Ideal Strength**.

Authors: Jiawen Yu, Chaohong Guan, Xiaoqing Liu, Yangshuai Wang, Hong Zhu and Xiaoqin Zeng.

## Contents

| Directory | Content |
|---|---|
| plots/ | Author-composed final Figures 1–7 (JPG) and supplementary Figures S1/S2 |
| data/ | Extracted DFT references, input structures and six-model predictions |
| analysis/ | Numerical tables and final 48-element coverage source rows |
| code/ | Analysis and analytical-panel reproduction scripts |
| notebooks/ | Six model notebooks, extraction and shared calculation code |
| envs-setting/ | Six original Conda exports |
| metadata/ | Model identities, hashes, runtime and source provenance |
| model/ | Six selected local checkpoints; excluded from Git and upload ZIP |

## Dataset scope

Bulk relaxation/elasticity: 3,098 references; vacancy: 100 pairs; surface: 504 slabs;
efficiency: 100 mixed inputs; tensile: Al, Cu, Mo, W (NequIP uses nequip1).
The active SFE data exclude I1 and Po. All six models have 109 matched pairs;
the main 108-pair analysis additionally excludes the flagged MgCa I2 reference.
The extra pair and numerical sensitivity remain disclosed for verification.
Figure 2 uses 48 metallic species, counted from 3,814 explicit task cases.

Final composed JPGs in plots/ are the author's artwork. Scripts regenerate
analytical panels into ignored results/ and do not overwrite these final images.
They do not claim to reproduce every manually assembled layout pixel for pixel.
See REPRODUCE.md and analysis/README.md for precise scopes and commands.

## Quick start

    pip install -r requirements-analysis.txt
    python data/verify_data.py
    python code/reproduce_paper.py --task all --output results/paper_reproduction
    python code/plot_fig5c_nonI1.py
    python code/plot_fig2b_coverage.py
    python code/update_SI_radar.py

Use separate model environments for inference. Notebook example manifests are
schemas, not complete paper datasets. DFT settings are described in the final
manuscript/SI; licensed VASP binaries and POTCAR are not distributed.

## Models and environment

NequIP-OAM-XL, MACE-MPA-0 medium, SevenNet-Omni-i12, DPA-3.1-3M-FT,
CHGNet 0.3.0 and MatterSim 1.0.0-5M are identified in metadata/models.csv.
Six selected local checkpoints have recorded hashes. model/ is Git-ignored:
weight redistribution and download sources must be checked separately.
SevenNet and NequIP exceed normal Git file-size limits; do not force-add them.

Reported hardware: one RTX 4090 (24 GB), 10 vCPU, 60 GB RAM, Ubuntu 24.04.
Actual model Conda exports contain PyTorch 2.9.1 or 2.5.1+cu121; the reported
2.7.0 was the base-image description. The server NVIDIA driver is not recorded.

## Interpretation and limitations

Bulk-model final atomic coordinates were not saved. Hash checks do not certify
fresh checkpoint loading. The original global Figure 3 aggregate and all SI
static energy/force results are not fully reproduced by available-data scripts.
Figure 7b recalculates SFE only; seven other axes retain original authored
scores. Known reference flags/exclusions remain documented in data/sfe_nonI1/.

## Citation and permissions

Repository: https://github.com/jiaweny097-web/MLIP-Benchmark

Use CITATION.cff and cite the actual tag/commit used. No finalized release tag
or archival DOI is asserted by this local preparation. Original software is
licensed for noncommercial research/education (LICENSE-CODE.txt); original data
and documentation use CC BY-NC 4.0 (LICENSE-DATA.md). Third-party rights remain
with their owners; see THIRD_PARTY_NOTICES.md. This is source-available under
noncommercial terms. Public access and final manuscript correspondence should
be confirmed when publishing the reviewed files.

## Reproduction updates

Run python code/export_inputs.py --output inputs to generate the actual retained
input manifests and structures. See REPRODUCE.md for tested counts and commands.
Static Fig3/SI S3 differences and missing fields are documented in analysis/static/.
All eight radar axes have source/status records in analysis/fig7b/scoring_provenance.csv.
Weight download links are optional convenience metadata, not a new prerequisite.
