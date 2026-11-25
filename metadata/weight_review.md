# Selected checkpoint review

All six named checkpoints are now present. metadata/models.csv records the selected
path and SHA-256; local_weight_inventory.csv also records duplicates and alternatives.

DPA selected dpa-3.1-3m-ft.pth contains TorchScript code entries, consistent with the
supplied torch.jit.load adapter. The additional DPA-3.1-3M.pt is not substituted.
NequIP selected the compiled .pt2, not the unpacked package components.
MatterSim selected the root default_5M.pth; other5M copies are byte-identical.
MACE selected mace-mpa-0-medium.model. CHGNet and SevenNet filenames match original code.

Checks establish local byte identity and expected container format only; real model
loading/inference and original-server hashes have not been validated. Do not infer
download provenance or a license solely from filename. Obtain artifact source URLs
and retain original third-party notices.

SevenNet and NequIP exceed100MiB and cannot be stored in regular Git commits.
The entire model directory remains ignored pending a per-checkpoint redistribution
review and choice of upstream download links, Git LFS or an archive. Our noncommercial
original-work license does not restrict or replace third-party weight permissions.
