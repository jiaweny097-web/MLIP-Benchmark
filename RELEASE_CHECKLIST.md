# Release and Computational Materials Science submission check

Checked 2026-11-25 against the local release directory, original manuscript/SI,
the supplied editorial letter and previous release checklist. This is a local
artifact audit; public GitHub access and the latest journal web policy were not
revalidated in this pass. No manuscript DOCX or remote repository was modified.

## Current scope and completed work

- [x] Exclude all I1 and Po-containing records from active SFE database collections,
  including source tables, perfect pools and predictions. Recoverable originals
  are outside the upload repository, not bundled as data.
- [x] Pair non-I1 FCC ISF/ESF and HCP I2 by constrained input identity and same-type
  perfect lineage. Archive source IDs, component energies, areas and structures.
- [x] All six models have the same 109 matched pairs. The labelled 108-pair scope
  applies the author's prior MgCa I2 exclusion; the full 109-pair data remain.
  ZnTi I2 lacks a complete verified match; ZnMn I2 is absent from supplied v4.
- [x] Restore Figure 5c's error strip/boxplot and six-inset layout. MAE/RMSE/R2/MAPE
  are checked against the unchanged paired-data metrics. PNG/SVG/PDF supplied.
- [x] Recompute Figure 2b periodic-table coverage after I1/Po removal: original
  five-source scope and explicit current-release reference scope both supplied.
  Counts and source rows are provided; model outputs are not counted six times.
- [x] Six original tensile codes load simulation z and analyze sigma_zz. Repository
  figures use the author-selected nequip1 curves; original DOCX remains unchanged.
- [x] Six local selected checkpoints and six original/portable Conda exports exist
  and their SHA-256 values match recorded inventories in this audit.
- [x] Author-reported RTX4090 x1/24GB, 10vCPU, 60GB RAM, Ubuntu24.04 recorded.
  Per-model exports show PyTorch2.9.1 or2.5.1+cu121;2.7.0 is the reported base image.
- [x] Noncommercial original-work license files, third-party reservations,
  CITATION.cff, extracted plain-data PKLs and integrity catalogs are present.

## Data and analysis still requiring resolution

- [ ] Decide the final manuscript SFE scope. The current release omits I1. A paper
  still reporting full I1 results needs matching final DFT/model calculations,
  or its text/figures/sample counts must reflect the non-I1 scope. Exclusion here
  is not a claim that final I1 results have been reproduced.
- [ ] Resolve or explicitly discuss flagged DFT references: MgCa I2 gives about
  -45284mJ/m2; MgY I2 has positive component total energies. Other large values
  are retained. Positive absolute energy alone does not prove invalidity.
- [ ] Supply real task manifests or a tested builder for inference from released
  inputs. notebooks/config/manifest_examples still contains example rows only.
- [ ] Finish exact reproduction mapping for every final figure and SI table.
  Global Figure3, exact Fig7b layout and complete SI analyses are not established
  by current generic available-data entry points. Non-I1 Fig5c and coverage Fig2b
  now have explicit tested commands; they do not resolve all other panels.
- [ ] Align final manuscript/SI with current sample scopes and values: SFE counts,
  Fig2b counting population, tensile sigma_zz and nequip1 values, and previously
  recorded Cauchy-count/rate differences. No manuscript rewrite was authorized here.
- [ ] Identify actual pseudopotential dataset names/versions and all applicable
  settings in the final manuscript/SI. The inspected original DOCX/SI describe
  VASP/GGA-PBE and a settings table, but no explicit PAW/POTCAR identifiers were
  found in their visible text. Referencing the paper is sufficient only when
  those details are actually in the submitted version; do not distribute POTCAR.
- [x] Disclose absent bulk-model relaxed atomic coordinates/full predicted tensors.
  The author reports saving CSV summaries only. This is a documented limitation,
  not an instruction to fabricate coordinates or upload unavailable output files.

## Models, provenance and access still requiring completion

- [ ] Add checkpoint-specific download URLs/releases and original artifact
  notices. metadata/models.csv currently links project homepages, not precise
  downloadable checkpoint artifacts with verified third-party licenses.
- [ ] Confirm upstream data/weight reuse terms and required attributions. The
  noncommercial grant covers author-owned work only. Materials Project, surface,
  HEA and tensile-source notices remain explicitly unconfirmed in
  THIRD_PARTY_NOTICES.md; per-element tensile acquisition/digitization notes
  also remain to be supplied or verified.
- [ ] Validate actual checkpoint loading and an energy/force/stress example per
  model. Hash/container checks are not inference tests. No such GPU test was run.
- [ ] Record the actual compute server NVIDIA driver and external package indices
  if absent from exports. Local Windows driver information is not a substitute.
- [ ] Choose checkpoint distribution (upstream artifact links, Git LFS or archive).
  model/ is ignored; SevenNet and NequIP exceed normal Git's100MiB file limit.
  The upload ZIP intentionally excludes model weights.
- [ ] Commit and publish the reviewed current data/plots, then cite the exact
  commit/tag (optional archival DOI). The local repository has a remote and a
  commit, but no release tag and uncommitted changes in this audit. No public
  access/release publication is claimed.
- [ ] Update the final manuscript Data Availability to public data/code links and
  the actual fixed version, and test access without author credentials. The
  inspected original manuscript still says available upon reasonable request.

## Separate editorial-system files

The editor's supplied letter requires these submission items, not necessarily
public GitHub files:

- [ ] Separate Highlights:3-5 bullets, at most85 characters including spaces each.
- [ ] Editable revised manuscript source and matching final SI/figure files.
- [ ] Point-by-point response uploaded as Response to Reviewers, with actual data
  and code access links and an accurate description of the submitted scope.

No standalone Highlights/Response files were found in the inspected workspace
root; that does not establish whether they exist elsewhere or in Editorial Manager.
Full OUTCAR/WAVECAR trees are not requested by this checklist. Provide extracted
inputs/results and enough documented settings and runnable code to verify claims.

## Reproduction commands for this update

    python data/verify_data.py
    python data/sfe_v4/recompute.py
    python code/plot_fig5c_nonI1.py
    python code/plot_fig2b_coverage.py

See analysis/fig2b/README.md and data/sfe_nonI1/README.md for exact populations.
The earlier six-panel parity charts are supplementary diagnostic artifacts;
Fig5c_SFE_nonI1_*.png/svg/pdf are the requested Figure5c-style outputs.

## Previous guidance sources (not re-fetched in this local audit)

- Supplied editorial letter in this conversation.
- https://www.sciencedirect.com/journal/computational-materials-science/publish/guide-for-authors
- https://www.elsevier.com/en-in/researcher/author/tools-and-resources/research-data/data-guidelines
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
