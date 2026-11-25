# Release and Computational Materials Science submission check

Checked2026-11-24. This audit distinguishes the specific editor request, verified
publisher guidance and reproducibility recommendations. The full ScienceDirect
Guide for Authors returned403, so its current detailed data-policy option and
every formatting requirement could not be independently read. Do not use another
journal named "Computational Materials Science" at Frontiers as this journal's policy.

## Needed for this manuscript's completeness

- [ ] Complete final HCP I1 DFT and matching six-model results, then release a final
  fault/perfect pairing manifest preserving same-type directory lineage.
- [ ] Finish FCC/I2 pairing review; current sfe_partial is extracted/unpaired data,
  not a finalized SFE evaluation or reproduction of the revised paper.
- [ ] Provide real task manifests or a tested builder from current PKLs, and exact
  analysis/plot commands for each manuscript figure and SI table. Current notebook
  CSV templates are examples; the global Fig3 aggregate is incomplete while I1 is absent.
- [x] Verified six original tensile codes load simulation z and analyze σzz;
  repository entry points and figures are aligned to that axis.
- [ ] Update the manuscript's prior xx labels and NequIP values before submission.
  No DOCX file was changed in the current repository-only update.
- [x] DFT settings are referred to the manuscript and Supporting Information, as requested by the author.
- [ ] Ensure the final manuscript/SI actually identifies the applicable pseudopotential family/versions and all task-specific settings before submission.
- [ ] Confirm code/prediction/manuscript synchronization after final reruns. Cleaned
  generic notebooks are future-rerun implementations, not proof of historical fidelity.

## Models and runtime

- [x] Six local checkpoint files identified, sized and hashed.
- [x] Author-reported RTX4090x1/24GB,10vCPU,60GB RAM,Ubuntu24.04,PyTorch2.7.0 recorded.
- [ ] Add original checkpoint download URLs/releases and artifact-specific notices.
- [x] Export actual Conda package sets for all six model environments.
- [ ] Add NVIDIA driver and any external pip-index/channel details not captured by
  the environment exports.
- [ ] Validate real checkpoint loads and a small energy/force/stress example per model.
- [ ] Choose model distribution strategy. model/ remains ignored; SevenNet and
  NequIP exceed100MiB. Upstream links+hashes can avoid redistributing these files.

## Rights and citation

- [x] Author chose noncommercial research permission: custom software license and
  CC BY-NC4.0 for original data/documentation, excluding third-party rights.
- [ ] Confirm all relevant rights-holder/institutional approvals and original
  upstream dataset/model terms. Do not apply new commercial restrictions to
  third-party rights that you do not own.
- [x] CITATION.cff and fixed-release instructions provided, without fictional DOI/version.
- [ ] After final review, publish an actual tag/commit and optionally an archived
  DOI (recommended for persistent citation; not asserted as a universal journal mandate).
- [ ] Update manuscript Data Availability and dataset citation with working public
  links and the exact release used. Check reader access without author credentials.

## Manuscript files requested by the editor, separate from GitHub

The supplied editorial letter requires a separate Highlights file (3–5 points,
maximum85 characters including spaces each), editable manuscript source files,
and a point-by-point document uploaded as "Response to Reviewers". These are
submission-system items; they need not be public repository files. Upload the
current SI, figures and tables consistently with the revised manuscript.

The editor specifically required all appropriate supporting data/code at submission
and preferred GitHub. Merely having a README or publicly visible code does not
establish complete support for results still missing from the dataset.

## What does not need to be uploaded automatically

Complete OUTCAR/WAVECAR/vasprun.xml trees, VASP binaries/POTCAR, personal local
backups, caches, .env files, and every historical experiment are not automatically
required. Supply sufficient extracted results, inputs, settings and runnable analysis
for verification; if an extraction omitted information needed for a stated result,
provide that missing subset or explain the limitation. Bulk final coordinates were
not saved: disclose that fact rather than fabricate them or imply they are available.

## Sources

- Journal official scope/policy: https://shop.elsevier.com/journals/computational-materials-science/0927-0256
- Guide for Authors (full fetch blocked during audit): https://www.sciencedirect.com/journal/computational-materials-science/publish/guide-for-authors
- Elsevier data guidelines: https://www.elsevier.com/en-in/researcher/author/tools-and-resources/research-data/data-guidelines
- Data statement: https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-statement
- License meaning: https://creativecommons.org/licenses/by-nc/4.0/
- Citation metadata: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
- File size limits: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

## Available analyses completed 2026-11-24

- [x] Added REPRODUCE.md and a tested code/reproduce_paper.py entry point for available data.
- [x] Recorded six original Conda exports and portable copies, with actual package versions.
- [x] Verified all six selected local checkpoint hashes without loading model objects.
- [x] Preserved unavailable/pending analyses explicitly rather than claiming full paper reproduction.
