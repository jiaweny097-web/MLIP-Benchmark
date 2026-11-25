"""Recompute Fig3-style available subsets and SI S3 with explicit metric scope."""
from pathlib import Path
import argparse,json,pickle
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
MODELS=['nequip','mace','sevennet','dpa','chgnet','mattersim']
def load(rel):
    with (ROOT/'data'/rel).open('rb') as f:return pickle.load(f)['records']
def rmse(e):return float(np.sqrt(np.mean(np.asarray(e)**2))) if len(e) else None
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'results/static_reproduction');args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
    rows=[];issues=[];by_model={m:dict(energy=[],force=[]) for m in MODELS}
    surface_ref={r['ID']:r for r in load('surface/dft/reference.pkl')}
    for model in MODELS:
        for task in ['bulk','vacancy','surface']:
            energy=[];force=[];basis='total energy divided by atom count'
            if task in ['bulk','vacancy']:
                name='static_bulk' if task=='bulk' else 'static_vacancy'
                records=load('static calculation/'+name+'/predictions/'+model+'.pkl')
                for r in records:
                    e,d=('energy_per_atom_eV','DFT_energy_per_atom_eV') if task=='bulk' else ('energy_eV','DFT_energy_eV')
                    n=1 if task=='bulk' else r['atom_count']
                    if r.get(e) is not None and r.get(d) is not None:energy.append((r[e]-r[d])/n)
                    x,y=r.get('forces_eV_A'),r.get('DFT_forces_eV_A')
                    if x is None or y is None:continue
                    x=np.asarray(x,float);y=np.asarray(y,float);assert x.shape==y.shape
                    err=(x-y).ravel();force.extend(err[np.isfinite(err)].tolist())
                if task=='bulk':basis='archived energy already eV/atom'
            else:
                records=load('surface/predictions/'+model+'.pkl')
                for r in records:
                    ref=surface_ref[r['ID']];n=len(ref['structure']['atomic_numbers'])
                    # Matches original plot.ipynb cell17. This is the normalized
                    # surface-energy difference, not absolute slab-energy error.
                    err=(r['ml_surface_energy_J_m2']-r['dft_surface_energy_J_m2'])*r['area_A2']*(1e-20/1.602176634e-19)/n
                    if np.isfinite(err):energy.append(err)
                basis='surface-energy difference times area times0.06241509 / slab atom count; original Fig3 convention'
                issues.append(dict(task=task,model=model,missing='DFT forces absent from released surface references; force RMSE unavailable'))
            rows.append(dict(task=task,model=model,N_energy=len(energy),Energy_RMSE_eV_atom=rmse(energy),N_force_components=len(force),Force_RMSE_eV_A=rmse(force),energy_basis=basis))
            by_model[model]['energy'].extend(energy);by_model[model]['force'].extend(force)
    pd.DataFrame(rows).to_csv(out/'SI_Table_S3_available_subsets.csv',index=False)
    global_rows=[]
    for model,v in by_model.items():global_rows.append(dict(model=model,N_energy=len(v['energy']),energy_RMSE_eV_atom=rmse(v['energy']),N_force_components=len(v['force']),force_RMSE_eV_A=rmse(v['force']),scope='available subsets only; SFE absent and surface DFT forces unavailable; NOT original full Fig3'))
    pd.DataFrame(global_rows).to_csv(out/'Fig3_available_subset_aggregate.csv',index=False)
    for model in MODELS:issues.append(dict(task='sfe',model=model,missing='Current108-pair formation inputs/results are relaxed-pair data, not matched original static energy/force records; do not substitute them'))
    pd.DataFrame(issues).to_csv(out/'missing_static_data.csv',index=False)
    (out/'scope.json').write_text(json.dumps(dict(original_source='benchmark-data-并行/plot.ipynb cell17 and user-supplied original Fig3 code',energy_unit='eV/atom',force_unit='eV/angstrom',full_original_Fig3_reproduced=False,original_SI_Table_S3_reproduced=False,surface_energy_metric='normalized surface-energy error; not raw slab energy',missing=['matched SFE static snapshots/predictions for current retained subset','surface DFT force arrays if original force aggregate used them'],no_inference=True),indent=2),encoding='utf-8')
    print(pd.DataFrame(rows).to_string(index=False));print('Full original Fig3/Table S3 NOT claimed; missing fields explicitly exported.')
if __name__=='__main__':main()
