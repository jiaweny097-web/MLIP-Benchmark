# Consolidated extracted benchmark data

Only aggregated PKL files and small documentation/indexes are included. No OUTCAR,
vasprun.xml, POSCAR trees, electronic restart binaries, per-sample checkpoint folders
or intermediate historical releases are included.

Layout: TASK/dft/reference.pkl, TASK/predictions/MODEL.pkl. Additional role files are
explicitly named. Each file is a standard-library pickle envelope with schema_version,
task, role, dataset_status, units, metadata, sources and records. Records contain plain
dict/list/scalar objects only. ASE and pymatgen classes, calculators and model graphs
are not embedded. Numpy arrays are converted to lists. POSCAR/CIF inputs are represented
as normalized structural arrays or explicit source text where appropriate.

Read a trusted local file with pickle.load(open(path,"rb")) and inspect envelope["records"].
Pickle must not be loaded from untrusted sources. catalog.csv gives counts/checksums;
data_status.csv states scientific missing fields and unresolved provenance.

Tasks:
- bulk_elastic:3098 reference inputs and six3098-row prediction tables joined by material_id.
- static_bulk:3098 single-point energy/force records per model; bulk energies are eV/atom.
- vacancy:100 paired formation-energy records, input/relaxed structures and chemical potentials.
- static_vacancy:archived snapshot DFT/model collections, separate from relaxed vacancy energies.
- surface:504 slab references and six504-entry prediction sets; J/m2 and mJ/m2 labels explicit.
- efficiency:100 mixed inputs and six100-entry speed result sets with step/time/convergence data.
- tensile:four DFT literature curves, initial CIF structures and six model curve collections;
  NequIP uses nequip1, selected by the author. Source stress-axis labels are preserved.
- sfe_partial:historical FCC and HCP I2 source-extracted data only; I1 omitted from this collection.
  No legacy derived SFE metrics are promoted; reference pairing still requires final path review.
- sfe_v4:129 directory-paired DFT references from the updated fault summary, including final
  I1 input structures and separate model-version audits. 125 pairs do not contain Po.
  Flagged energies are preserved; this is not a completed six-model I1 evaluation.

No missing structure is fabricated from its DFT reference. Bulk model relaxed coordinates
and tensile per-strain atomic structures are absent in the supplied summaries, and are
marked accordingly. The SFE perfect pools are unpaired shared records, not a completed
I1 benchmark. Do not confuse raw numeric IDs with physical pair identities.

This organization does not recalculate scientific values or resolve the documented
data-quality questions. Full prior data and original simulations remain backed up
outside the upload repository; historical exclusion records remain in metadata.

Surface update:504 slab and matched-bulk total energies are included in surface/dft/reference.pkl, verified by (E_slab-E_bulk_matched)/(2A). Maximum reconstruction residual is below9e-8 J/m2. The matched bulk energy has been scaled to the slab atom count; absolute energy zeroes need not match uMLIP totals.
