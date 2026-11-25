from pathlib import Path
import argparse,csv,pickle,math
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'results/static_metrics.csv');a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);out=[]
 for task in ['static_bulk','static_vacancy']:
  for m in ['nequip','mace','sevennet','dpa','chgnet','mattersim']:
   with (ROOT/'data'/'static calculation'/task/'predictions'/(m+'.pkl')).open('rb') as f:rows=pickle.load(f)['records']
   ek,dk=('energy_per_atom_eV','DFT_energy_per_atom_eV') if task=='static_bulk' else ('energy_eV','DFT_energy_eV')
   e=[float(r[ek])-float(r[dk]) for r in rows if r.get(ek) is not None and r.get(dk) is not None]
   out.append(dict(task=task,model=m,N=len(e),RMSE=math.sqrt(sum(x*x for x in e)/len(e)),unit='eV/atom' if task=='static_bulk' else 'eV',scope='retained subset only; not original Fig3 aggregate'))
 with a.output.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 print('Only retained static subsets exported; final I1 pending, global Fig3 not reproduced.')
if __name__=='__main__':main()
