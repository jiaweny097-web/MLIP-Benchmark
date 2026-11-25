from pathlib import Path
import argparse,csv,json,pickle,math
ROOT=Path(__file__).resolve().parents[1]
def read(rel):
 with (ROOT/'data'/rel).open('rb') as f:return pickle.load(f)['records']
def metrics(y,p):
 e=[b-a for a,b in zip(y,p)];n=len(e);mean=sum(y)/n;v=sum((x-mean)**2 for x in y)
 return dict(N=n,MAE=sum(map(abs,e))/n,RMSE=math.sqrt(sum(x*x for x in e)/n),R2=1-sum(x*x for x in e)/v if v else None)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'results/consolidated');a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 vr={r['ID']:r['formation_energy_eV'] for r in read('vacancy/dft/reference.pkl')}
 sr={r['ID']:r['DFT_surface_energy_mJ_m2'] for r in read('surface/dft/reference.pkl')}
 rows=[]
 for m in ['nequip','mace','sevennet','dpa','chgnet','mattersim']:
  v=read('vacancy/predictions/'+m+'.pkl');s=read('surface/predictions/'+m+'.pkl')
  rows.append(dict(task='vacancy',model=m,unit='eV',**metrics([vr[r['ID']] for r in v],[r['formation_energy_eV'] for r in v])))
  rows.append(dict(task='surface',model=m,unit='mJ/m2',**metrics([sr[r['ID']] for r in s],[r['model_surface_energy_mJ_m2'] for r in s])))
 with (a.output/'vacancy_surface_metrics.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (a.output/'efficiency_summary.json').write_text(json.dumps(read('efficiency/summaries/pareto_metrics.pkl'),indent=2))
 print('Computed twelve metric rows and exported source efficiency summary; final I1 remains pending.')
if __name__=='__main__':main()
