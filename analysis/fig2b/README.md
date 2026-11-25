# Figure2b element coverage — 2026-11-25

The original plot is cell114 of benchmark-data-并行/data-extract.ipynb. Its
five-source population differs from the current publication reference population.
Two outputs are supplied rather than silently mixing those counts:

- original_source_scope:1801 cases =1393 original classify-new bulk rows +100 HEA
  rows +100 vacancy rows +100 sampled surface rows +108 retained non-I1 SFE pairs.
  This follows the original source choices and metal-presence count convention.
- release_reference_scope:3814 cases =3098 current bulk references +100 vacancy
  pairs +504 surface slabs +108 retained SFE pairs +4 tensile element references.
  This is the coverage of the explicitly listed publication reference tasks,
  not a reconstruction of the earlier manuscript's undocumented full corpus.

Each case contributes once per distinct metallic species, independent of atom
count. A vacancy/SFE pair contributes its perfect-input composition once. Each
model's predictions are not counted again. Static copies of bulk/vacancy and
efficiency mixed inputs are not added again. There is no global geometry dedup
across distinct task cases; the same composition in separate tasks may count twice.
Metalloids/nonmetals are grey following the original metal-only plot convention.
I1 and Po are absent from both populations; SFE uses the108-pair scope with MgCa
I2 excluded. Source rows, task labels and counts are provided in CSV for inspection.

The original-scope plot contains59 metallic species; the current-release scope
contains48. Different source populations, rather than merely I1 deletion, account
for this difference. Match the final Figure2 caption and manuscript to the chosen
population. Reproduce with `python code/plot_fig2b_coverage.py`.
