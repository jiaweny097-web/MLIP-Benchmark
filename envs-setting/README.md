# Author-supplied Conda exports

Six original exports are preserved. portable/ copies change only name to mlip-MODEL
and remove the original absolute prefix, leaving dependency pins unchanged.

On a compatible Linux GPU host:
    conda env create -f envs-setting/portable/mace-environment.yml
    conda activate mlip-mace

Repeat with the chosen model. These Linux exports include architecture-specific
packages. CUDA-tagged pip wheels may require the corresponding PyTorch wheel index;
the export does not record every external channel/index or driver setting.

metadata/environment_exports.json summarizes actual versions. PyTorch is2.9.1 in
four supplied environments and2.5.1+cu121 in DPA/SevenNet, differing from the previously
reported base-image2.7.0. Both facts are retained rather than overwriting the exports.
Conda package version and pretrained model version are separate concepts (for example
CHGNet software0.4.2 may load a model checkpoint labeled0.3.0).

The exports were not installed or GPU-tested during repository preparation.
