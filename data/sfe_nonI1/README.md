# Stacking fault energy data

One collection contains 109 physical pairs with results for all six models.
The main-paper scope is 108 pairs, excluding MgCa I2 as recorded by
previous_author_exclusion in paired_model_results.csv. The extra pair stays
available to quantify the exclusion effect, not as a second dataset version.
I1 and Po-containing structures are absent. ZnTi I2 lacks a complete model
match; ZnMn I2 has no supplied v4 fault result. Exclusions are documented.

reference.pkl contains matched perfect/fault inputs, POSCAR text, DFT energies,
area and sources. MODEL.pkl contains relaxed structures and energies. ID/pair_key
connects both states and all models. The paired CSV exposes component energies.
SFE=(E_fault-E_perfect)/area*16021.76634 mJ/m2, using one fault area.

pairing_audit.csv records identity matches and selected raw IDs. For identical
Al perfect inputs, original export order resolves isf IDs 1–26 versus esf IDs
27–52; energy never chooses candidates. Saved cells/compositions were checked.
Convergence and all reference-quality questions are not certified. MgCa I2 is
flagged/excluded in main analysis. MgY I2 positive component energies remain
flagged but included. No additional error-based exclusion is imposed.
