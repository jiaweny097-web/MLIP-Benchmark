"""Figure 5c layout: signed-error strip/box plot with six parity insets."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
MODELS=['nequip','mace','sevennet','dpa','chgnet','mattersim']
NAMES=['NequIP','MACE','SevenNet','DPA-3-FT','CHGNet','MatterSim']
COLORS=['#F3891C','#F8AD63','#FDE1C7','#4874CB','#A1BEE4','#E0E7FF']

def main():
    data=pd.read_csv(ROOT/'data/sfe_nonI1/paired_model_results.csv')
    data=data[data.six_model_common]
    out=ROOT/'results/sfe_nonI1'
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'Arial','svg.fonttype':'none','pdf.fonttype':42})
    metrics=[]
    for scope,df in [('all_matched',data),('without_MgCa_I2',data[~data.previous_author_exclusion])]:
        rng=np.random.default_rng(0)
        fig=plt.figure(figsize=(15,10))
        # Original Figure 5c geometry and type sizes, including cropped width.
        left,bottom,width,height=.12,.14,.726,.52
        ax=fig.add_axes([left,bottom,width,height])
        errors=df.ML_sfe_mJ_m2-df.DFT_sfe_mJ_m2
        bound=10**np.ceil(np.log10(max(float(abs(errors).max())*1.4,201)))
        ax.set_yscale('symlog',linthresh=200)
        ax.set(xlim=(-.5,5.5),ylim=(-bound,bound))
        ax.axhline(0,color='#666666',ls='--',lw=1,alpha=.5)
        inset_bound=10**np.ceil(np.log10(max(float(df.DFT_sfe_mJ_m2.abs().max()),float(df.ML_sfe_mJ_m2.abs().max()),201)))
        arrays=[]
        for i,(m,n,c) in enumerate(zip(MODELS,NAMES,COLORS)):
            d=df[df.model==m]; y=d.DFT_sfe_mJ_m2.to_numpy();p=d.ML_sfe_mJ_m2.to_numpy();e=p-y
            arrays.append(e)
            ax.scatter(i+rng.uniform(-.32,.32,len(d)),e,s=45,color=c,alpha=.4,edgecolors='none',zorder=3)
            mae=np.mean(abs(e));den=np.sum((y-y.mean())**2);r2=1-np.sum(e**2)/den
            nonzero=abs(y)>1e-12;mape=100*np.mean(abs(e[nonzero]/y[nonzero]))
            ax.text(i,.94,f'MAE = {mae:.1f}',transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=17)
            top=fig.add_axes([left+width*i/6+.004,bottom+height+.03,width/6-.012,.18])
            top.set_xscale('symlog',linthresh=200);top.set_yscale('symlog',linthresh=200)
            top.set(xlim=(-inset_bound,inset_bound),ylim=(-inset_bound,inset_bound),xticks=[],yticks=[])
            top.plot([-inset_bound,inset_bound],[-inset_bound,inset_bound],color='#888888',lw=1)
            top.scatter(y,p,s=5,color=c,alpha=.65)
            top.text(.04,.97,f'$R^2 = {r2:.2f}$',transform=top.transAxes,va='top',fontsize=11)
            top.text(.96,.035,f'MAPE = {mape:.1f}%',transform=top.transAxes,ha='right',fontsize=11)
            top.tick_params(which='both',length=0)
            for spine in top.spines.values():spine.set_linewidth(1.2)
            metrics.append(dict(scope=scope,model=m,N=len(d),MAE_mJ_m2=mae,RMSE_mJ_m2=np.sqrt(np.mean(e**2)),R2=r2,MAPE_percent=mape))
        ax.boxplot(arrays,positions=range(6),widths=.18,showfliers=False,
            boxprops=dict(color='#222222',linewidth=1.8),whiskerprops=dict(color='#222222',linewidth=1.8),
            capprops=dict(color='#222222',linewidth=1.8),medianprops=dict(color='#A62424',linewidth=2.5))
        ax.set_xticks(range(6),NAMES,rotation=35,ha='right',fontsize=20)
        ax.set_ylabel(r'$\Delta\gamma_{\mathrm{SF}}$ (mJ m$^{-2}$)',fontsize=20)
        ax.tick_params(axis='y',labelsize=16,direction='in',length=6)
        ax.grid(axis='y',color='#E5E7EB',alpha=.5)
        for spine in ax.spines.values():spine.set_linewidth(1.5)
        fig.text(.483,.91,'I1 excluded' + ('; MgCa I2 excluded' if scope=='without_MgCa_I2' else '; all matched pairs'),ha='center',fontsize=13)
        for extension in ['jpg']:
            fig.savefig(out/f'Fig5c_SFE_nonI1_{scope}.{extension}',dpi=350,bbox_inches='tight',transparent=True)
        plt.close(fig)
    table=pd.DataFrame(metrics)
    table.to_csv(out/'Fig5c_metrics.csv',index=False)
    reference=pd.read_csv(ROOT/'analysis/sfe_nonI1/Fig5c_metrics.csv')
    np.testing.assert_allclose(table[['MAE_mJ_m2','RMSE_mJ_m2','R2','MAPE_percent']],reference[['MAE_mJ_m2','RMSE_mJ_m2','R2','MAPE_percent']])
    print('PASS: Figure 5c composite style; metrics identical to paired-data evaluation.')

if __name__=='__main__':main()
