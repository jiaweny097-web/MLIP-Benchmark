# Extracted benchmark data

Aggregated trusted PKLs contain schema_version, task, role, dataset_status,
units, metadata, sources and records. Records use plain dict/list/scalar values,
without live ASE/pymatgen calculators. No raw OUTCAR or restart trees are included.
catalog.csv records counts, sizes and SHA-256. Run python data/verify_data.py.

Tasks: bulk_elastic (3,098 references), static calculation/static_bulk and
static_vacancy, vacancy (100 pairs), surface (504 slabs and 286 bulk references),
efficiency (100 mixed inputs), tensile (Al/Cu/Mo/W), sfe_nonI1 (109 matched
pairs; 108 in the main-paper analysis). See task fields for units/structures.
Bulk model relaxed atomic coordinates were not saved; none are fabricated.

Energy is eV, length angstrom, force eV/angstrom. Surface/SFE units are explicit.
Source paths are provenance, not runnable paths on another computer. Missing
values are not zero. Only deserialize trusted pickle files. data_status.csv
records availability limitations.
