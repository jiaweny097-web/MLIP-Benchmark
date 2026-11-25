# Static energy and force reproduction

Run python code/reproduce_static_metrics.py. The available-subset table uses
the original Fig3 convention: bulk energies are eV/atom, vacancy total-energy
differences are divided by atom count, and surface-energy errors are converted
by area and atom count. Surface here is a normalized surface-energy metric,
not unaligned slab total-energy error. Missing force values are unavailable,
not zero. Bulk has3091 finite energy pairs in the current records.

Vacancy/surface energy values agree with the original SI S3 at displayed
precision. Bulk does not: e.g. MACE0.01576 versus original SI0.0044 eV/atom.
Original single-point-v2 archived data reproduce the released result. The old
single-point files contain incompatible/mixed energy conventions and are not
silently substituted. The original SI population/filter/reference convention
still requires reconciliation; its numbers are not certified by this table.

Current SFE formation-energy inputs/predictions cannot substitute for archived
single-point force tests. Legacy static SFE exists in the workspace, but its
stored DFT energies differ from the updated reference for multiple compositions.
No attempt is made to relabel old snapshot results as predictions on newly
relaxed DFT snapshots. Thus the full original Fig3 and all S3 rows remain
unresolved. See missing_static_data.csv; no final figures were changed.
