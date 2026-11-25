"""Recompute available paper analyses from consolidated PKLs, never rerun inference."""
from pathlib import Path
import argparse,json,pickle,sys
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code/reproduce'))
MODELS=['nequip','mace','sevennet','dpa','chgnet','mattersim']
NAMES=['NequIP','MACE','SevenNet','DPA-3-FT','CHGNet','MatterSim']
COLORS=['#F3891C','#F8AD63','#FDE1C7','#4874CB','#A1BEE4','#C4CCE8']
def load(rel):
    with (ROOT/'data'/rel).open('rb') as f:return pickle.load(f)['records']
def metric(y,p):
    y=np.asarray(y,float);p=np.asarray(p,float);e=p-y;v=sum((y-y.mean())**2);nz=abs(y)>1e-12
    return dict(N=len(y),MAE=float(np.mean(abs(e))),RMSE=float(np.sqrt(np.mean(e*e))),R2=float(1-sum(e*e)/v) if v else np.nan,MAPE_percent=float(np.mean(abs(e[nz]/y[nz]))*100) if nz.any() else np.nan)
def savefig(fig,out,name):
    fig.savefig(out/(name+'.jpg'),dpi=250,bbox_inches='tight')
    plt.close(fig)
def paired():
    ref=pd.DataFrame(load('bulk_elastic/dft/reference.pkl')).set_index('ID',verify_integrity=True)
    classes=pd.read_csv(ROOT/'metadata/material_structure_classes.csv').set_index('material_id')
    ref['class']=classes.structure_type
    tensors=np.array(ref.elastic_tensor.tolist(),float)
    for name,i,j in [('C11',0,0),('C12',0,1),('C44',3,3)]:ref[name]=tensors[:,i,j]
    for m in MODELS:
        pred=pd.DataFrame(load('bulk_elastic/predictions/'+m+'.pkl')).set_index('ID',verify_integrity=True)
        if set(pred.index)!=set(ref.index):raise ValueError('Bulk IDs mismatch')
        yield m,ref,pred.loc[ref.index]
def bulk(out):
    rows=[];excluded=[];metallurgy=[]
    mapping={'lattice_a':'lattice_a','lattice_b':'lattice_b','lattice_c':'lattice_c','B_VRH':'B_Voigt_Reuss_Hill','G_VRH':'G_Voigt_Reuss_Hill','C11':'C11','C12':'C12','C44':'C44'}
    for m,ref,p in paired():
        for prop,col in mapping.items():
            y=pd.to_numeric(ref[col],errors='coerce');v=pd.to_numeric(p[m+'_'+prop],errors='coerce')
            valid=np.isfinite(y)&np.isfinite(v)
            for group in ['All','FCC','BCC','HCP','Other']:
                mask=valid if group=='All' else valid&(ref['class']==group)
                for mode in ['all_finite','original_MAPE_le_50']:
                    keep=mask.copy()
                    if mode=='original_MAPE_le_50':keep &= abs((v-y)/(y+1e-9))*100<=50
                    if keep.any():rows.append(dict(model=m,property=prop,structure=group,filter=mode,N_before_error_filter=int(mask.sum()),**metric(y[keep],v[keep])))
        b=pd.to_numeric(p[m+'_B_VRH'],errors='coerce');g=pd.to_numeric(p[m+'_G_VRH'],errors='coerce')
        valid=np.isfinite(b)&np.isfinite(g)&(g!=0)
        for ID in ref.index[~valid]:excluded.append(dict(model=m,material_id=ID,reason='Missing/nonfinite B or G, or zero G'))
        y=(ref.B_Voigt_Reuss_Hill/ref.G_Voigt_Reuss_Hill).to_numpy(float);v=(b/g).to_numpy(float);ok=valid.to_numpy()&np.isfinite(y)&np.isfinite(v)
        c12=pd.to_numeric(p[m+'_C12'],errors='coerce');c44=pd.to_numeric(p[m+'_C44'],errors='coerce')
        cubic=ref['class'].isin(['FCC','BCC']).to_numpy()&np.isfinite(c12)&np.isfinite(c44)
        metallurgy.append(dict(model=m,N_Pugh=int(ok.sum()),Pugh_MAE=float(np.mean(abs(v[ok]-y[ok]))),ductility_misclassification_percent=float(100*np.mean((v[ok]>1.75)!=(y[ok]>1.75))),N_Cauchy=int(cubic.sum()),Cauchy_sign_inversion_percent=float(100*np.mean(np.sign((c12-c44)[cubic])!=np.sign((ref.C12-ref.C44)[cubic])))))
    a=pd.DataFrame(rows);a.to_csv(out/'bulk_lattice_elastic_metrics.csv',index=False)
    pd.DataFrame(excluded).to_csv(out/'SI_invalid_elastic_pairs.csv',index=False)
    pd.DataFrame(metallurgy).to_csv(out/'Table2_metallurgical_metrics.csv',index=False)
    # Show original thresholded and unfiltered results explicitly; no silent removal.
    for mode in ['all_finite','original_MAPE_le_50']:
        fig,axes=plt.subplots(1,2,figsize=(12,4))
        heat=a[(a.structure=='All')&(a['filter']==mode)&a.property.isin(['B_VRH','G_VRH','C11','C12','C44'])].pivot(index='model',columns='property',values='MAPE_percent').reindex(MODELS)[['B_VRH','G_VRH','C11','C12','C44']]
        im=axes[0].imshow(heat,cmap='YlOrRd',aspect='auto')
        axes[0].set_xticks(range(5),heat.columns);axes[0].set_yticks(range(6),NAMES);fig.colorbar(im,ax=axes[0],label='MAPE (%)')
        for i in range(6):
            for j in range(5):axes[0].text(j,i,f'{heat.iloc[i,j]:.1f}',ha='center',va='center',fontsize=8)
        lattice=a[(a['filter']==mode)&a.structure.isin(['FCC','BCC','HCP','Other'])&a.property.str.startswith('lattice')]
        # Original grouped workflow weights property means by pre-error-filter Count.
        for k,m in enumerate(MODELS):
            vals=[]
            for group in ['FCC','BCC','HCP','Other']:
                sub=lattice[(lattice.model==m)&(lattice.structure==group)]
                vals.append(np.average(sub.MAPE_percent,weights=sub.N_before_error_filter) if len(sub) else np.nan)
            axes[1].bar(np.arange(4)+(k-2.5)*.12,vals,width=.12,label=NAMES[k],color=COLORS[k])
        axes[1].set_xticks(range(4),['FCC','BCC','HCP','Other']);axes[1].set_ylabel('Weighted lattice MAPE (%)');axes[1].legend(fontsize=7,ncol=2)
        fig.suptitle('Available bulk results: '+mode);fig.tight_layout()
        savefig(fig,out,'Fig3c_Fig4_available_'+mode)
def defects(out):
    rows=[];fig,axes=plt.subplots(2,1,figsize=(10,7));rng=np.random.default_rng(0)
    ref={r['ID']:r['formation_energy_eV'] for r in load('vacancy/dft/reference.pkl')}
    for i,m in enumerate(MODELS):
        for task in ['vacancy','surface']:
            records=load(task+'/predictions/'+m+'.pkl')
            y=[ref[r['ID']] if task=='vacancy' else r['dft_surface_energy_J_m2']*1000 for r in records]
            v=[r['formation_energy_eV'] if task=='vacancy' else r['model_surface_energy_mJ_m2'] for r in records]
            stats=metric(y,v);rows.append(dict(task=task,model=m,**stats))
            e=np.array(v)-np.array(y);ax=axes[0 if task=='vacancy' else 1]
            ax.scatter(i+rng.uniform(-.25,.25,len(e)),e,s=7,alpha=.3,c=COLORS[i]);ax.boxplot([e],positions=[i],widths=.2,showfliers=False)
    for ax,unit in zip(axes,['Vacancy error (eV)','Surface error (mJ/m²)']):
        ax.axhline(0,c='gray',ls='--',lw=.6);ax.set_xticks(range(6),NAMES);ax.set_ylabel(unit)
    fig.tight_layout();savefig(fig,out,'Fig5ab_vacancy_surface')
    pd.DataFrame(rows).to_csv(out/'Fig5ab_metrics.csv',index=False)
def tensile(out):
    from tensile_original_metrics import compute_metrics_for_one_model
    rows=[];peak=[]
    from tensile_original_metrics import read_archived_curve,get_peak
    for el in ['Mo','W','Cu','Al']:
        fig,ax=plt.subplots(figsize=(6.4,4.8))
        x,y=read_archived_curve('dft',el);ax.plot(x*100,y,'k--',label='DFT reference')
        upper=float(np.max(x))
        if el=='Al':
            upper=max(float(np.max(read_archived_curve(m,el)[0])) for m in MODELS)
        _,dft_peak_x,dft_peak_y=get_peak(x,y,el)
        ax.scatter(dft_peak_x*100,dft_peak_y,marker='*',s=95,c='black',zorder=5)
        for k,m in enumerate(MODELS):
            mx,my=read_archived_curve(m,el)
            visible=(mx>=0)&(mx<=upper)
            px,py=mx[visible],my[visible]
            if len(px) and px[-1]<upper and mx.min()<=upper<=mx.max():
                px=np.append(px,upper);py=np.append(py,np.interp(upper,mx,my))
            ax.plot(px*100,py,label=NAMES[k],c=COLORS[k])
            r=compute_metrics_for_one_model(el,'brittle' if el in ['Mo','W'] else 'ductile',m)
            if r is None:raise ValueError('Tensile metric calculation failed')
            rows.append(r)
            ax.scatter(r['ML_peak_strain_%'],r['ML_peak_stress_GPa'],s=24,
                       facecolors='white',edgecolors=COLORS[k],zorder=4)
        ax.set_xlim(0, upper*100)
        ax.set_title(el);ax.set_xlabel('Engineering strain (%)');ax.set_ylabel(r'Tensile stress $\sigma_{zz}$ (GPa)')
        fig.tight_layout();savefig(fig,out,'Fig6_'+el+'_sigmaZZ')
    a=pd.DataFrame(rows);a.to_csv(out/'tensile_curve_metrics_by_element.csv',index=False)
    means=a.groupby('Model_key').mean(numeric_only=True);means.to_csv(out/'Table3_curve_metrics_mean.csv')
    for m,sub in a.groupby('Model_key'):
        peak.append(dict(model=m,**metric(sub.DFT_peak_stress_GPa,sub.ML_peak_stress_GPa)))
    pd.DataFrame(peak).to_csv(out/'Table3_peak_stress_metrics.csv',index=False)
    peak_index=pd.DataFrame(peak).set_index('model')
    combined=[]
    for m in ['mace','nequip','mattersim','dpa','chgnet','sevennet']:
        v=peak_index.loc[m];c=means.loc[m]
        combined.append(dict(Model=NAMES[MODELS.index(m)],MAE_GPa=v.MAE,RMSE_GPa=v.RMSE,
            MAPE_percent=v.MAPE_percent,Relative_E_error_percent=c['E001_relative_error_%'],
            NIASE_percent=c['NIASE_%'],Relative_strain_energy_error_percent=c['Strain_energy_relative_error_%']))
    pd.DataFrame(combined).to_csv(out/'Table3_all_six_metrics.csv',index=False)
    a[['Element','Model','Model_key','DFT_peak_stress_GPa','ML_peak_stress_GPa',
       'DFT_peak_strain_%','ML_peak_strain_%']].to_csv(out/'tensile_peak_values.csv',index=False)
def efficiency(out):
    rows=[]
    for m in MODELS:
        a=load('efficiency/predictions/'+m+'.pkl')
        times=[r['time_per_step'] for r in a if r.get('time_per_step') is not None]
        rows.append(dict(model=m,N=len(a),success_rate_percent=100*np.mean([r['converged'] for r in a]),mean_time_per_step_s=float(np.mean(times)),zero_step_count=sum(r['total_steps']==0 for r in a)))
    a=pd.DataFrame(rows)
    a['pareto_nondominated']=[not any((b.success_rate_percent>=r.success_rate_percent and b.mean_time_per_step_s<=r.mean_time_per_step_s and (b.success_rate_percent>r.success_rate_percent or b.mean_time_per_step_s<r.mean_time_per_step_s)) for _,b in a.iterrows()) for _,r in a.iterrows()]
    a.to_csv(out/'Fig7_efficiency_pareto.csv',index=False)
    fig,ax=plt.subplots(figsize=(7,4))
    for k,r in a.iterrows():
        ax.scatter(r.success_rate_percent,r.mean_time_per_step_s,c=COLORS[k]);ax.annotate(NAMES[k],(r.success_rate_percent,r.mean_time_per_step_s),xytext=(3,4),textcoords='offset points')
    ax.set_xlabel('Success rate (%)');ax.set_ylabel('Source mean time per step (s)');fig.tight_layout();savefig(fig,out,'Fig7a_efficiency')
def static(out):
    rows=[]
    for task in ['static_bulk','static_vacancy']:
        for m in MODELS:
            r=load('static calculation/'+task+'/predictions/'+m+'.pkl')
            key,ref=('energy_per_atom_eV','DFT_energy_per_atom_eV') if task=='static_bulk' else ('energy_eV','DFT_energy_eV')
            rows.append(dict(task=task,model=m,metric='energy',unit='eV/atom' if task=='static_bulk' else 'eV',**metric([x[ref] for x in r],[x[key] for x in r])))
            e=[];y=[];p=[]
            for x in r:
                a=x.get('DFT_forces_eV_A');b=x.get('forces_eV_A')
                if a is None or b is None:continue
                aa=np.array(a,float);bb=np.array(b,float)
                if aa.shape!=bb.shape:raise ValueError('Force shape mismatch')
                y.extend(aa.flatten());p.extend(bb.flatten())
            if len(y):rows.append(dict(task=task,model=m,metric='force_components',unit='eV/angstrom',**metric(y,p)))
    pd.DataFrame(rows).to_csv(out/'static_task_metrics_only.csv',index=False)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--task',choices=['all','bulk','defects','tensile','efficiency','static'],default='all');ap.add_argument('--output',type=Path,default=ROOT/'results/paper_reproduction');a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    tasks=dict(bulk=bulk,defects=defects,tensile=tensile,efficiency=efficiency,static=static)
    for name,fn in tasks.items():
        if a.task in ['all',name]:print('Recomputing:',name);fn(a.output)
    (a.output/'scope.json').write_text(json.dumps(dict(scope='available consolidated data only',pending=['final I1/SFE evaluation','global Fig3 aggregate','Fig2 original full-corpus composition count','SI SFE perfect/fault total energy analysis'],tensile_axis='source stress_zz_gpa retained',bulk_filters=['all_finite','original_MAPE_le_50'],efficiency='original arithmetic mean of stored time_per_step including source zero-step convention'),indent=2))
if __name__=='__main__':main()
