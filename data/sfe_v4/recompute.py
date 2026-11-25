"""Reconstruct DFT SFE from the trusted portable reference without ASE."""
from pathlib import Path
import csv
import math
import pickle

root = Path(__file__).resolve().parent
with (root / 'dft_reference.pkl').open('rb') as stream:
    records = pickle.load(stream)['records']
rows = []
for r in records:
    value = (r['energy_fault_eV'] - r['energy_perfect_eV']) / r['area_A2'] * 16021.76634
    assert math.isclose(value, r['sfe_mJ_m2'], abs_tol=1e-8)
    rows.append(dict(ID=r['ID'], pair_key=r['pair_key'], sfe_mJ_m2=value,
                     quality=r['quality'], excluded_reason=r['excluded_reason']))
with (root / 'recomputed_sfe.csv').open('w', encoding='utf-8', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f'PASS: reconstructed {len(rows)} unique paired DFT SFE values.')
