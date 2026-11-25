# Clean benchmark notebooks

Six model notebooks share benchmark_workflows.py and dpa_adapter.py. Each has eight
complete task sections: static energy/forces, bulk relaxation, elastic tensor/VRH,
vacancy energy, SFE, unrelaxed surface energy, efficiency and ideal tensile response.

## Running

Use a separate compatible environment per model. Install requirements.txt here and
the selected model package. Set CHECKPOINT, DEVICE and checkpoint-specific options.
Prepare input CSVs using config/manifest_examples. Example rows are schemas, not
manuscript data. Enable LOAD_MODEL and only the required RUN flags. Defaults do not
load a checkpoint or run inference. Results go to new results/notebook-reruns paths.
Task, input-file and checkpoint hashes reject incompatible resumed calculations.

DPA needs its actual species-to-type mapping or checkpoint get_type_map. No guessed
atomic-number mapping or fallback checkpoint is used. SevenNet may need an explicit
modal in MODEL_OPTIONS. NequIP requires an ASE-target compiled model compatible with
the installed runtime. Checkpoints are not bundled.

## Numerical and scientific conventions

- Fixed cell preserves POSCAR atomic constraints; it does not by itself constrain
  in-plane atomic motion. Validate the final I1 geometry and F F T flags.
- Final I1 and I1-old must not be mixed. This cleanup does not complete pending runs.
- SFE and vacancy input tables identify explicit fault/perfect paths. No same-number
  subtraction, formula-only pairing or hidden exclusion is used.
- SFE=(E_fault-E_perfect)/area/fault_planes*16021.7733, mJ/m2.
- Vacancy=E_vac-E_perfect+mu_removed; supply the chemical-potential convention.
- Surface energy is unrelaxed slab/bulk subtraction with explicit surface count.
- Elasticity uses centered +/-1% engineering strains, all6 independent components,
  ASE Voigt order xx yy zz yz xz xy, full6x6 stress response in GPa and VRH averaging.
  Strained internal coordinates are clamped; no implicit cubic/hexagonal projection.
- Tensile default is z-axis (`axis=2`), matching the six original implementations:
  extend `cell[2,2]`, relax the transverse x/y normal strains, and read σzz.
  Input z must align with the intended crystal direction. The supplied conventional
  cubic cells use [001], symmetry-equivalent to the other ⟨100⟩ directions.
  The cleaned workflow retains ASE tensile-positive stress without the historical
  automatic sign-flip heuristic; optimizer-history details also differ. Matching
  the loading axis alone does not certify exact historical inference reproduction.
- DPA finite-difference stress computes dE/dstrain at fixed fractional coordinates,
  costs12 additional energy evaluations per stress and needs step/precision convergence
  checks for the actual checkpoint. Native virial is opt-in and assumes eV.
- Efficiency reports convergence, steps and GPU-synchronized times, excluding model
  loading. Do not count capped nonconverged runs as successful or impute missing errors.
- Model stress implementations and element coverage must be checked in each runtime.

## Supporting files

data-extract.ipynb: explicit pair validation and DFT zero-smearing energy extraction.
error analysis.ipynb: paired metric evaluation with strict ID joins.
plot.ipynb: selected table plotting and verified Figure3 script entry point.

Historical adsorption/Mg-H2O work, BCC GSFE trials, manuscript generation, duplicate
API-acquisition experiments and old plotting/structure utilities were removed from
this notebook collection. Full backups are outside the repository. Original workspace
notebooks and all existing scientific data remain untouched.

The consolidated code is for new runs. It does not certify pending final-I1 runs,
supply missing model environments, or relabel historical results as reproduced.

SFE/vacancy paired tasks intentionally recompute pairs on a repeated invocation so that the per-run unique-perfect cache is not mixed with an earlier optimizer state. Other converged tasks can resume by matching run signature. Nonconverged records are retried. CHGNet device keyword and SevenNet import path are resolved explicitly for the installed API.
