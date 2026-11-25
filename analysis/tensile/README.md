# Tensile results aligned to simulation z / sigma_zz

Recomputed from the unchanged consolidated curves, using the author-selected
NequIP nequip1 variant and the original numerical peak/integration functions.
Four separate figures display sigma_zz for Mo, W, Cu and Al. Their maximum plotted
strains are15%,48%,48% and50%, respectively. Mo/W/Cu use the DFT limits;
Al uses the maximum available model-test strain. No legends are displayed. Model curves are not
extrapolated beyond their available data. This display change does not alter the
evaluation interval or metrics. All six original model notebooks explicitly load
simulation z; metadata/tensile_axis_evidence.csv at repository root records the
source cells and hashes. These four input cells are conventional cubic cells;
[001] is symmetry-equivalent to the cubic <100> family, but simulation axes and
crystal-direction labels are different concepts.

Table3_all_six_metrics.csv contains the six metrics together. NequIP is now
0.976,1.083,5.041,13.91,6.60,6.32 at the manuscript precision. The Mo/W NequIP
peaks are26.48/29.47GPa. Other five model rows agree with the previous table at
its displayed precision. Metric-specific rankings are unchanged.

Command: python code/reproduce_paper.py --task tensile --output analysis/tensile

Additional combined figure: `python code/plot_tensile_combined.py` produces
`Fig6_combined_sigmaZZ.png`, `.svg` and `.pdf` in this directory. The 2-by-2
panel order is Mo/W above Cu/Al, with one shared legend below the panels.
It uses the same archived curves, plotting limits and original peak function;
the separate figures remain available without legends.

This refreshes tables and figures from stored curves; no model inference was
rerun. The original force/stress arrays are unmodified. The cleaned inference
default is axis=2; its other optimizer-history and sign-handling conventions
remain documented differences from the historical code. W peak identification
uses the first decreasing stress segment, as in the original metric function.

No manuscript DOCX was changed, at the author's request. Previous manuscript
axis labels, table values and peak descriptions require a separate future edit.
Final I1/SFE remains pending and is unaffected by this tensile update.
