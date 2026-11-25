# SFE DFT v4 update — 2026-11-25

The author-supplied fault v4 summary contains 129 entries. Each is paired by
crystal, host, fault type and alloy directory with perfect-summary_results-v2.csv,
not by row order or numeric ID. All 129 pairs are preserved; 125 do not contain Po.
SFE IDs identify this complete extraction, not a finalized evaluation subset.
ZnNi I1 is absent (author reports nonconvergence); ZnMn I2 is also absent from v4.
The latter is recorded as missing without inventing a cause.

Formula: (E_fault - E_perfect) / |a1 cross a2| * 16021.76634 mJ/m2.
The one-fault-area convention follows the historical calculation; no extra factor
of two is introduced. Energies are copied from the summary Energy column.
The summaries do not certify convergence. Input POSCARs, not newly downloaded
relaxed structures, are provided with each energy. Local OUTCAR/CONTCAR files
predate the reported rerun and are not presented as its outputs.

The perfect v2 table still contains positive MgCa reference energies (I1/I2),
producing approximately -34615/-45284 mJ/m2. MgY I2 also has positive total
energies. These are flagged for source review, not silently declared invalid.
MgY I1 and ZnCu I1 are now approximately 158.36 and 46.03 mJ/m2; old four-row
exclusions must not be reapplied by numeric ID after the v4 renumbering.
No new primary filtered subset is imposed in this extraction.

The input-version audit compares full constrained geometry, and separately
species-resolved fixed x/y coordinates and cell (ignoring movable z). The saved
six-model result audit checks actual relaxed structures and stored constraints.
See CSV statuses for coverage. Old evaluation numbers are not relabeled as
final-v4 I1 predictions. No model inference was rerun and no DOCX was modified.

PKL uses plain Python dictionaries/lists/scalars, including fault/perfect input
structures, POSCAR text, component energies, area, source paths and source IDs.
Original summaries are retained under sources for independent checking.
The historical sfe_partial collection remains available pending model alignment.

The author confirmed no updated Perfect summary is available. Final I1 rerun
inputs are under inputs/: two ID-to-POSCAR-text PKLs (15 pairs) and one manifest.
These are plain input dictionaries compatible with the original inference
loops, distinct from the enveloped result collection. Including these files
does not imply reruns have been performed. Recompute stored DFT values with
`python data/sfe_v4/recompute.py`.
