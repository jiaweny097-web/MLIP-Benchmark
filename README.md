# MLIP-Benchmark

Data and code supporting **Evaluating Universal Interatomic Potentials for Metallic Systems: From Elastic Response to Defect Energetics and Ideal Strength**.

**Authors:** Jiawen Yu, Chaohong Guan, Xiaoqing Liu, Yangshuai Wang, Hong Zhu and Xiaoqin Zeng.

This benchmark evaluates six universal interatomic potentials for metallic structures, elastic response, defects, ideal tensile deformation and computational efficiency. The repository provides extracted numerical/structural data rather than full VASP output directories.

**Status:** release preparation in progress. The 2026-11-25 DFT SFE v4 update is available in `data/sfe_v4` (129 directory-paired records, 125 without Po). Matching final I1 model predictions and flagged DFT references remain unresolved; see its README and audits. This snapshot is not a complete reproduction of every manuscript result. No article acceptance, DOI or finalized release is asserted.

## Repository structure

    MLIP-Benchmark/
    ├── data/
    │   ├── bulk_elastic/          # Bulk inputs, relaxation/elastic predictions
    │   ├── static calculation/
    │   │   ├── static_bulk/       # Bulk single-point energies/forces
    │   │   └── static_vacancy/    # Vacancy snapshot energies/forces
    │   ├── vacancy/               # Paired formation energies and structures
    │   ├── surface/               # Slab/bulk structures and surface energies
    │   ├── efficiency/            # Mixed inputs, convergence and timing
    │   ├── tensile/               # DFT literature/model stress-strain curves
    │   ├── sfe_partial/           # Historical FCC/HCP I2 model/source records
    │   ├── sfe_v4/                # Updated paired DFT, structures and model audits
    │   ├── catalog.csv            # Paths, counts, status and SHA-256
    │   ├── data_status.csv        # Missing fields and limitations
    │   └── verify_data.py         # Integrity and numerical checks
    ├── notebooks/                 # Six model notebooks and shared workflows
    ├── code/                      # Lightweight analysis entry points
    ├── metadata/                  # Models, hardware and weight inventory
    ├── model/                     # Local downloads, currently Git-ignored
    ├── CITATION.cff
    ├── LICENSE
    ├── LICENSE-CODE.txt
    ├── LICENSE-DATA.md
    ├── THIRD_PARTY_NOTICES.md
    ├── RELEASE.md
    └── RELEASE_CHECKLIST.md

## Dataset coverage

| Task | Reference/input size | Prediction coverage | Qualification |
|---|---:|---|---|
| Bulk relaxation and elasticity | 3,098 material IDs | Six models, 3,098 rows each | Final model atomic coordinates/full predicted tensors absent from source CSV |
| Static bulk | 3,098 structures | Six models | Bulk energies are per atom; reference forces may be absent |
| Vacancy formation | 100 pairs | Six models, 100 entries each | Component energies and available input/relaxed structures retained |
| Static vacancy | 100 archived snapshots | Six model collections | Exact snapshot correspondence needs verification |
| Surface | 504 slabs; 286 bulk structures | Six models, 504 surface-energy entries each | DFT bulk energy matched to slab atom count |
| Relaxation efficiency | 100 mixed inputs | Six models, 100 entries each | Author-selected mixed_relaxation_benchmark-speed source |
| Tensile response | Al, Cu, Mo, W | Four curves per model | NequIP uses author-selected nequip1 |
| SFE | 129 v4 DFT directory pairs; 125 without Po | Historical model collections; final I1 alignment pending | ZnNi I1 nonconverged; ZnMn I2 absent; flagged references retained |

Counts describe supplied/extracted records, not proof of scientific validity. Status fields and units must be checked before use.

## Models

| Model | Manuscript version | Historical checkpoint filename |
|---|---|---|
| DPA-3-FT | DPA-3.1-3M-FT | dpa-3.1-3m-ft.pth |
| NequIP | NequIP-OAM-XL | mir-group__NequIP-OAM-XL__0.1.nequip.pt2 |
| MACE | MACE-MPA-0 medium | mace-mpa-0-medium.model |
| SevenNet | SevenNet-Omni-i12 | checkpoint_sevennet_omni_i12.pth |
| CHGNet | 0.3.0 | chgnet_0.3.0_e29f68s314m37.pth.tar |
| MatterSim | 1.0.0-5M | default_5M.pth |

Names were recovered from original calculation code. Downloaded files are not automatically certified as the exact historical artifacts. See [model metadata](metadata/models.csv), [local checkpoint hashes](metadata/local_weight_inventory.csv) and [weight review](metadata/weight_review.md).

All six selected checkpoint files are now available locally, with hashes recorded. The selected DPA FT file has the expected TorchScript container; the extra DPA-3.1-3M.pt is a different artifact and is not selected. NequIP uses the compiled .pt2 rather than unpacked model components. MatterSim copies are byte-identical. SevenNet and NequIP exceed the100MiB ordinary Git limit. The model directory remains ignored pending identity, redistribution and storage review; do not force-add it blindly.

## Read the PKL files

There are67 catalogued PKL collections. Each is a standard Python dictionary containing schema_version, task, role, dataset_status, units, metadata, sources and records. Structures and scientific fields are plain dictionaries/lists/scalars, without live ASE/pymatgen calculators. Two additional final-I1 input PKLs under `data/sfe_v4/inputs` use simple ID-to-POSCAR-text dictionaries compatible with the original inference scripts; their matching IDs are listed in `final_I1_manifest.csv`.

    from pathlib import Path
    import pickle

    with Path("data/surface/dft/reference.pkl").open("rb") as stream:
        dataset = pickle.load(stream)
    print(dataset["task"], dataset["dataset_status"])
    print(len(dataset["records"]))
    print(dataset["records"][0].keys())

Only deserialize pickle from trusted sources. Missing fields are None, not zero. Structure fields include atomic numbers/symbols, cell/lattice parameters, Cartesian/fractional coordinates, periodicity and constraints. CIF source text is explicitly labeled. Historical source paths are provenance, not runnable paths on another computer.

## Validate and analyze supplied results

Run from the repository root:

    python data/verify_data.py
    python code/analyze_results.py --output results/consolidated
    python code/reproduce_fig3_metrics.py --output results/static_metrics.csv

The first command requires only the Python standard library and checks hashes, counts, paired IDs, vacancy differences and surface-energy reconstruction. The second recomputes vacancy/surface metrics and exports the supplied efficiency summary. The third exports retained static task subsets only; it does not reconstruct the original global Figure3 aggregate while final I1 is absent.

These checks do not rerun VASP or model inference and do not establish physical validity of every reference.

For a figure/table-level map of the currently reproducible analyses, commands and
outputs, see [REPRODUCE.md](REPRODUCE.md).

## Run a model

Use separate compatible environments for the six model frameworks.

    python -m pip install -r notebooks/requirements.txt
    python -m pip install jupyterlab

Install the selected model package, then open its notebook. Set CHECKPOINT, DEVICE and model-specific options; create real task input CSVs from the documented schemas. Enable LOAD_MODEL, then only the required RUN task. All flags default to False.

Each model notebook exposes eight tasks: static energy/forces, bulk relaxation, elastic tensor/VRH, vacancy formation, SFE, unrelaxed surface energy, relaxation efficiency and tensile response. Shared code is in notebooks/benchmark_workflows.py; DPA uses dpa_adapter.py. Input templates in notebooks/config/manifest_examples are schema examples, not completed paper manifests. Outputs use new results/notebook-reruns directories with input, model and protocol fingerprints.

See [notebook instructions](notebooks/README.md). These are consolidated future-rerun implementations. Analytic-calculator tests validate generic numerical workflows; real six-checkpoint runs have not been validated by this repository preparation.

## Units and protocols

- Total energy: eV; bulk per-atom energy: eV/atom; lengths: Å; forces: eV/Å.
- Surface/SFE fields explicitly distinguish J/m² and mJ/m².
- Vacancy formation: E_vacancy − E_perfect + chemical potential of removed species.
- Two-surface reference: (E_slab − E_bulk_matched)/(2A). Matched bulk total corresponds to the slab atom count.
- SFE: (E_fault − E_perfect)/(A × number_of_fault_planes) ×16021.7733, in mJ/m².
- Fault/perfect pairing preserves composition, fault family, input geometry, constraints and original source lineage. Same-numbered filenames alone do not define a pair.
- Absolute energy zeroes differ among DFT/model methods; compare consistently matched energy differences, not cross-method absolute totals.
- Clean elastic code uses six centered engineering-strain components and VRH, with clamped internal coordinates in strained states; no implicit crystal-symmetry projection.
- The six original tensile implementations increase `cell[2,2]`, relax the transverse x/y normal strains, and analyze `stress_zz_gpa`: the simulated loading axis is z and the axial stress is σzz. The cleaned inference notebooks now default to `axis=2` for this same axis. For the supplied conventional cubic inputs the z direction is [001], a member of the symmetry-equivalent ⟨100⟩ family. This axis correction does not by itself make other optimizer details identical to the historical implementation.

## Author-reported compute environment

| Resource | Actual configuration |
|---|---|
| GPU | One NVIDIA RTX4090,24GB VRAM |
| CPU | 10vCPU |
| System memory | 60GB |
| OS | Ubuntu24.04 |
| Framework | PyTorch2.7.0 |

Six author-supplied Conda exports are included in `envs-setting/`, with portable
copies under `envs-setting/portable/`. They record the actual Python/model-package,
PyTorch, ASE and related dependency versions. Four exports contain PyTorch 2.9.1;
DPA and SevenNet contain PyTorch 2.5.1+cu121. The earlier PyTorch 2.7.0 value is
retained as an author-reported base-image description and is not substituted for
these per-environment exports. NVIDIA driver and some external pip-index details
remain unavailable. See [environment metadata](metadata/environment_exports.json).

## Provenance and availability

Data sources include Materials Project ([Jain et al.](https://doi.org/10.1063/1.4812323)), the surface dataset ([Schindler et al.](https://doi.org/10.1002/adfm.202401764)), the alloy source ([Li et al.](https://doi.org/10.1039/D4TA00982G)) and the manuscript's element-specific tensile references. Exact acquisition versions/archive links and upstream terms need final confirmation; see [third-party notices](THIRD_PARTY_NOTICES.md).

Only extracted data are distributed. Complete OUTCAR/vasprun.xml and VASP restart binaries are not needed in this compact repository; compact DFT settings, energy conventions and pseudopotential identifiers should still accompany reproducible results. Licensed VASP binaries/POTCAR are not included.

## Known limitations before the manuscript release

- Final HCP I1 DFT, matched predictions and final SFE pair manifest are pending.
- Model-relaxed bulk atomic coordinates were not saved; lattice parameters alone cannot uniquely reconstruct them.
- Tensile per-strain atomic structures are absent. The recorded source loading axis has been verified as z/σzz; the earlier DOCX versions still require the corresponding text/figure corrections and are not modified by this repository update.
- Some static vacancy snapshots differ from relaxed formation-energy states.
- Available bulk, vacancy/surface, tensile and efficiency analyses have a tested entry point in REPRODUCE.md; final SFE, the original Fig2 composition count and original global Fig3/SFE SI analyses remain incomplete.
- DFT settings are documented in the manuscript/SI. All six environment exports and selected local checkpoint hashes are included; actual checkpoint execution still requires validation.

See [release checklist](RELEASE_CHECKLIST.md). None of these gaps is filled with fabricated coordinates, identifiers or URLs.

## Citation and fixed release

[CITATION.cff](CITATION.cff) identifies this work. Cite the exact published tag/commit and the associated article when available. A finalized version, article DOI and archival dataset DOI have not yet been assigned. [RELEASE.md](RELEASE.md) explains immutable release citation and archiving.

The configured remote is [jiaweny097-web/MLIP-Benchmark](https://github.com/jiaweny097-web/MLIP-Benchmark). This local preparation does not establish public availability, push changes, or create a release.

## Noncommercial licensing

Original software is available for noncommercial research/education under [LICENSE-CODE.txt](LICENSE-CODE.txt). Original data/documentation are [CC BY-NC4.0](LICENSE-DATA.md). Commercial use requires separate permission. This is a noncommercial source-available release, not OSI-approved open source. Third-party data and weights retain their own terms.

Scientific contacts: Chaohong Guan (guanchaohong@sjtu.edu.cn), Hong Zhu (hong.zhu@sjtu.edu.cn), Xiaoqin Zeng (xqzeng@sjtu.edu.cn).
