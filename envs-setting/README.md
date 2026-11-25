# Model environments

Six original Conda exports are supplied; use separate environments per model:

    conda env create --name mlip-mace --file envs-setting/mace-environment.yml

Explicitly name the environment rather than reuse the original server prefix.
Versions/hashes are in metadata/environment_exports.json. Actual exports use
PyTorch 2.9.1 or 2.5.1+cu121; 2.7.0 was the author-reported base image. The
compute-server NVIDIA driver is not recorded.
