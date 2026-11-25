"""Recompute metrics and parity plots for the matched non-I1 SFE subset."""
from pathlib import Path
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
MODELS=['nequip','mace','sevennet','dpa','chgnet','mattersim']
NAMES=['NequIP','MACE','SevenNet','DPA-3-FT','CHGNet','MatterSim']
COLORS=['#F3891C','#F8AD63','#FDE1C7','#4874CB','#A1BEE4','#C4CCE8']

def main():
    data=ROOT/'data/sfe_nonI1'
    out=ROOT/'analysis/sfe_nonI1'
    out.mkdir(parents=True,exist_ok=True)
    frame=pd.read_csv(data/'paired_model_results.csv')
    common=frame[frame.six_model_common].copy()
    assert set(common.model)==set(MODELS)
    sets=[set(common.loc[common.model==m,'pair_key']) for m in MODELS]
    assert all(s==sets[0] for s in sets)
    # Check component-energy subtraction rather than plotting legacy derived values.
    np.testing.assert_allclose((common.ML_energy_fault_eV-common.ML_energy_perfect_eV)/common.area_A2*16021.76634,common.ML_sfe_mJ_m2,atol=1e-7)
    np.testing.assert_allclose((common.DFT_energy_fault_eV-common.DFT_energy_perfect_eV)/common.area_A2*16021.76634,common.DFT_sfe_mJ_m2,atol=1e-7)
    plt.rcParams.update({'font.family':'Arial','font.size':12,'svg.fonttype':'none','pdf.fonttype':42})
    metrics=[]
    for scope,subset in [('all_matched',common),('without_MgCa_I2',common[~common.previous_author_exclusion])]:
        fig,axes=plt.subplots(2,3,figsize=(12,8.2))
        values=np.concatenate([subset.DFT_sfe_mJ_m2,subset.ML_sfe_mJ_m2])
        low,high=float(values.min()),float(values.max())
        pad=max((high-low)*0.06,1)
        limits=(low-pad,high+pad)
        for ax,m,n,c in zip(axes.flat,MODELS,NAMES,COLORS):
            d=subset[subset.model==m]
            y=d.DFT_sfe_mJ_m2.to_numpy();p=d.ML_sfe_mJ_m2.to_numpy();e=p-y
            den=np.sum((y-y.mean())**2)
            metric=dict(scope=scope,model=m,N=len(d),MAE_mJ_m2=np.mean(abs(e)),RMSE_mJ_m2=np.sqrt(np.mean(e**2)),R2=1-np.sum(e**2)/den if den>0 else np.nan,
                MAPE_percent=100*np.mean(abs(e[abs(y)>1e-12]/y[abs(y)>1e-12])))
            metrics.append(metric)
            ax.plot(limits,limits,'k--',lw=1,zorder=1)
            ax.scatter(y,p,s=27,c=c,edgecolors='0.35',linewidths=.35,alpha=.85,zorder=2)
            ax.set(xlim=limits,ylim=limits,title=n,aspect='equal')
            ax.text(.04,.96,f"N = {len(d)}\nMAE = {metric['MAE_mJ_m2']:.2f}\nRMSE = {metric['RMSE_mJ_m2']:.2f}\n$R^2$ = {metric['R2']:.3f}",transform=ax.transAxes,va='top',fontsize=10)
            ax.tick_params(direction='in',top=True,right=True)
        for ax in axes[1,:]:ax.set_xlabel(r'DFT SFE (mJ m$^{-2}$)')
        for ax in axes[:,0]:ax.set_ylabel(r'Predicted SFE (mJ m$^{-2}$)')
        title='FCC ISF/ESF and HCP I2; I1 excluded'
        if scope=='without_MgCa_I2':title+='; MgCa I2 excluded'
        fig.suptitle(title,fontsize=14)
        fig.tight_layout(rect=(0,0,1,.96))
        for extension in ['png','svg','pdf']:
            fig.savefig(out/f'SFE_nonI1_{scope}.{extension}',dpi=350)
        plt.close(fig)
    pd.DataFrame(metrics).to_csv(out/'model_metrics.csv',index=False)
    common.to_csv(out/'all_model_results.csv',index=False)
    common[common.model==MODELS[0]][['ID','pair_key','DFT_sfe_mJ_m2','quality','previous_author_exclusion']].to_csv(out/'common_subset.csv',index=False)
    print(pd.DataFrame(metrics).to_string(index=False))

if __name__=='__main__':main()
