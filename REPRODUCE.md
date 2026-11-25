# Reproduce numerical results and analytical panels

Run commands from the repository root. Final author-composed Figures 1–7 are
plots/Fig1.jpg through Fig7.jpg. Code writes regenerated JPG panels and tables
to ignored results/; it does not overwrite manually assembled final artwork.

    python data/verify_data.py
    python code/reproduce_paper.py --task all --output results/paper_reproduction

Task choices: bulk, defects, tensile, efficiency, static. These calculate
available bulk/elastic, vacancy/surface, tensile and timing metrics. Static
analysis does not reconstruct the original global Figure 3 aggregate.

    python code/plot_fig2b_coverage.py
    python code/plot_fig5c_nonI1.py
    python code/plot_tensile_combined.py
    python code/update_SI_radar.py

Figure 2b uses the final 48-element/3,814-case source rows. Figure 5c uses 108
pairs in the main scope; the 109-pair sensitivity is also numerically available.
SI code computes Figure S1 perfect energies, S2 fault energies, Table S4 and
the SFE-only radar update. Table S3 static energy/force values are separate and
are not rederived by relaxed-energy analysis. See analysis/README.md.

Tensile uses sigma_zz and original numerical peak/integration functions with
the author-selected nequip1 data. Analysis scripts do not rerun inference.
For new calculations use the six notebooks, shared workflow and real input
manifests. config/manifest_examples contains schemas, not ready paper inputs.

    conda env create --name mlip-mace --file envs-setting/mace-environment.yml

Use an explicit new environment name rather than the original server prefix.
Repeat with each model export. Supply selected checkpoints identified in
metadata/models.csv; they remain outside Git/upload ZIP. DFT settings and
pseudopotential identifiers should be read from the submitted manuscript/SI.

## Actual input export and task lists

    python code/export_inputs.py --output inputs

This tested builder reads retained PKLs and creates real CSV task manifests
and deduplicated ASE JSON structure files. No model is loaded. Coordinates,
cell, species order, PBC and supported constraints are checked after export.
It creates bulk/elastic/static bulk3098 each, static vacancy100, vacancy100,
SFE108, surface504, efficiency100 and tensile4 input rows;4427 distinct
serialized structures in the tested export. static.csv defaults to bulk;
use static_vacancy.csv for that task. Original input arrays are preserved;
missing historical relaxed bulk coordinates are not reconstructed.

The existing six notebooks reference inputs/<task>.csv; run the builder before
enabling LOAD_MODEL and the chosen RUN flag. SFE is explicitly108 common pairs,
without I1/Po/MgCa I2. Surface exports matching bulk files. These are actual
retained input datasets for fresh calculations, not proof that cleaned future
optimizer/stress conventions reproduce historical trajectories exactly.

    python code/reproduce_static_metrics.py

The original Fig3 unit conventions are implemented for available bulk/vacancy/
surface subsets, with missing SFE/surface-force coverage documented separately.
See analysis/static/README.md for unresolved old SI bulk values. Never substitute
relaxed formation-energy data for a static energy/force test.

Figure7b provenance for all eight axes is in analysis/fig7b/scoring_provenance.csv.
Only the SFE aggregation is recovered as an explicit new formula. The source
notebook contains seven manually authored axes; no historical aggregate ranking
formula can be inferred from those numbers. Other axes and final artwork have
not been silently rescored. Weight download links are optional convenience
metadata; model/version/selected filename/hash and original citations remain.
