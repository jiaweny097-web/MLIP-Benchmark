"""Verify trusted consolidated PKLs without model, ASE or pymatgen imports."""
from pathlib import Path
import csv,hashlib,pickle,math
ROOT=Path(__file__).resolve().parent
def load(rel):
 with (ROOT/rel).open('rb') as f:return pickle.load(f)['records']
with (ROOT/'catalog.csv').open(encoding='utf-8',newline='') as f:catalog=list(csv.DictReader(f))
def basic(x):
 if x is None or type(x) in (str,int,float,bool):return
 if type(x) is list:
  for v in x:basic(v)
 elif type(x) is dict:
  for k,v in x.items():assert type(k) is str;basic(v)
 else:raise TypeError(type(x))
for r in catalog:
 p=ROOT/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 with p.open('rb') as f:o=pickle.load(f)
 basic(o);assert len(o['records'])==int(r['records'])
models=['nequip','mace','sevennet','dpa','chgnet','mattersim']
bulk={r['ID'] for r in load('bulk_elastic/dft/reference.pkl')};assert len(bulk)==3098
vac={r['ID']:r for r in load('vacancy/dft/reference.pkl')};assert len(vac)==100
for r in vac.values():assert math.isclose(r['DFT_vacancy_energy_eV']-r['DFT_perfect_energy_eV']+r['chemical_potential_eV'],r['formation_energy_eV'],abs_tol=1e-7)
speed={r['ID'] for r in load('efficiency/inputs/structures.pkl')};assert len(speed)==100
surface_rows=load('surface/dft/reference.pkl')
surface={r['ID'] for r in surface_rows};assert len(surface)==504
for r in surface_rows:
 calc=(r['DFT_slab_total_energy_eV']-r['DFT_bulk_reference_matched_total_energy_eV'])/(2*r['area_A2'])*16.02176634
 assert math.isclose(calc,r['DFT_surface_energy_J_m2'],abs_tol=1e-6,rel_tol=1e-6)
for m in models:
 assert {r['ID'] for r in load('bulk_elastic/predictions/'+m+'.pkl')}==bulk
 vv=load('vacancy/predictions/'+m+'.pkl');assert {r['ID'] for r in vv}==set(vac)
 for r in vv:
  assert math.isclose(r['vacancy_energy_eV']-r['perfect_energy_eV']+r['chemical_potential_eV'],r['formation_energy_eV'],abs_tol=1e-7)
 assert {r['ID'] for r in load('efficiency/predictions/'+m+'.pkl')}==speed
 assert {r['ID'] for r in load('surface/predictions/'+m+'.pkl')}==surface
 assert len(load('tensile/predictions/'+m+'.pkl'))==4
 sf=load('sfe_nonI1/'+m+'.pkl');assert len(sf)==109
 assert {r['pair_key'] for r in sf}.issubset({r['pair_key'] for r in load('sfe_nonI1/reference.pkl')})
 for r in sf:
  assert r['fault_type']!='I1' and 'Po' not in r['formula']
  assert math.isclose((r['ML_energy_fault_eV']-r['ML_energy_perfect_eV'])/r['area_A2']*16021.76634,r['ML_sfe_mJ_m2'],abs_tol=1e-7)
for r in load('sfe_nonI1/reference.pkl'):
 assert r['fault_type']!='I1' and 'Po' not in r['formula']
 assert math.isclose((r['energy_fault_eV']-r['energy_perfect_eV'])/r['area_A2']*16021.76634,r['sfe_mJ_m2'],abs_tol=1e-7)
print('PASS:',len(catalog),'standard-library-only PKLs; counts, IDs, vacancy energy formulas and I1 exclusion verified.')
