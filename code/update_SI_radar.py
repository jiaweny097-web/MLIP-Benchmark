"""SI S1/S2/S4 and original eight-axis Fig7b on the current108 SFE pairs."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
M=['nequip','mace','sevennet','dpa','chgnet','mattersim']
N=['NequIP','MACE','SevenNet','DPA-3-FT','CHGNet','MatterSim']
C=['#F3891C','#F8AD63','#FDE1C7','#4874CB','#A1BEE4','#E0E7FF']
plt.rcParams.update({'font.family':'Arial','svg.fonttype':'none','pdf.fonttype':42})
def save(fig,out,name):
    for ext in ['jpg']:fig.savefig(out/(name+'.'+ext),dpi=300,bbox_inches='tight')
    plt.close(fig)
def main():
    out=R/'results/SI';out.mkdir(parents=True,exist_ok=True)
    d=pd.read_csv(R/'data/sfe_nonI1/paired_model_results.csv');d=d[d.six_model_common&~d.previous_author_exclusion];assert len(d)==648
    assert all(len(d[d.model==m])==108 for m in M)
    rows=[]
    for role,num in [('perfect',1),('fault',2)]:
        fig,axes=plt.subplots(2,3,figsize=(12,8.5));yc='DFT_energy_'+role+'_eV';pc='ML_energy_'+role+'_eV'
        lo=min(d[yc].min(),d[pc].min());hi=max(d[yc].max(),d[pc].max());pad=(hi-lo)*.05
        for ax,m,n,c in zip(axes.flat,M,N,C):
            s=d[d.model==m];y=s[yc];p=s[pc];e=p-y;mae=abs(e).mean();rmse=np.sqrt(np.mean(e**2))
            rows.append(dict(model=m,Model=n,Structure=role,N=108,MAE_eV=mae,RMSE_eV=rmse,Mean_error_eV=e.mean()))
            ax.plot([lo-pad,hi+pad],[lo-pad,hi+pad],'k--',lw=1);ax.scatter(y,p,s=22,color=c,edgecolor='0.4',linewidth=.35,alpha=.75)
            ax.set(xlim=(lo-pad,hi+pad),ylim=(lo-pad,hi+pad),title=n,aspect='equal');ax.tick_params(direction='in',top=True,right=True)
            ax.text(.04,.96,f'MAE = {mae:.2f} eV\nRMSE = {rmse:.2f} eV',transform=ax.transAxes,va='top',fontsize=11)
        for ax in axes[1,:]:ax.set_xlabel('DFT total energy (eV)')
        for ax in axes[:,0]:ax.set_ylabel('Predicted total energy (eV)')
        fig.tight_layout();save(fig,out,f'Figure_S{num}_{role}_nonI1_108')
    t=pd.DataFrame(rows);t.to_csv(out/'Table_S4_nonI1_108.csv',index=False)
    cells=[[r.Model,r.Structure,'108',f'{r.MAE_eV:.2f}',f'{r.RMSE_eV:.2f}'] for r in t.itertuples()]
    fig,ax=plt.subplots(figsize=(10,5.5));ax.axis('off');tab=ax.table(cellText=cells,colLabels=['Model','Structure','N','MAE (eV)','RMSE (eV)'],loc='center',cellLoc='center');tab.auto_set_font_size(False);tab.set_fontsize(11);tab.scale(1,1.7);fig.tight_layout();save(fig,out,'Table_S4_nonI1_108')
    residuals=[]
    for m in M:
        s=d[d.model==m];ep=s.ML_energy_perfect_eV-s.DFT_energy_perfect_eV;ef=s.ML_energy_fault_eV-s.DFT_energy_fault_eV;e=ef-ep
        np.testing.assert_allclose(e/s.area_A2*16021.76634,s.ML_sfe_mJ_m2-s.DFT_sfe_mJ_m2,atol=1e-7)
        residuals.append(dict(model=m,N=108,energy_difference_MAE_eV=abs(e).mean(),energy_difference_RMSE_eV=np.sqrt(np.mean(e**2))))
    pd.DataFrame(residuals).to_csv(out/'energy_error_cancellation.csv',index=False);d.to_csv(out/'SI_energy_pairs.csv',index=False)
    (out/'README.md').write_text('108 pairs, excluding I1/Po/MgCa I2. Original SI numbering: Figure S1 perfect, S2 fault, Table S4 total energy. Table S3 is separate static energy/force data and is unchanged. Unaligned raw energies may include composition-dependent reference offsets. Residual energy-difference errors control SFE; component errors largely cancel. Original SI documents preserved. Run python code/update_SI_radar.py.\n',encoding='utf-8')
    out=R/'results/fig7b';out.mkdir(parents=True,exist_ok=True)
    t=pd.read_csv(R/'data/figure_sources/sfe_nonI1/Fig5c_metrics.csv');t=t[t.scope=='without_MgCa_I2'].set_index('model').loc[M].copy()
    cols=['MAE_mJ_m2','RMSE_mJ_m2','MAPE_percent','R2']
    for col in cols:t[col+'_rank']=t[col].rank(ascending=col!='R2')
    t['mean_rank']=t[[col+'_rank' for col in cols]].mean(axis=1);t['SFE_score']=11-t.mean_rank.rank();t.to_csv(out/'SFE_metric_ranks_and_scores.csv')
    original=np.array([[10,10,10,9,7,9,10,10],[8,8,9,8,9,10,9,9],[6,6,7,7,5,5,6,7],[9,9,8,10,10,7,8,5],[5,5,6,5,8,6,5,6],[7,7,5,6,6,8,8,8]],float)
    scores=original.copy();scores[:,3]=t.SFE_score.to_numpy()
    np.testing.assert_array_equal(scores[:,[0,1,2,4,5,6,7]],original[:,[0,1,2,4,5,6,7]])
    tasks=['Static simulation\nand structural optimization','Elastic properties','Vacancy formation\nenergy','Stacking-fault\nenergy','Surface energy','Ideal tensile\nstrength','Convergence\nsuccess rate','Time per step']
    for name,arr in [('original_authored_scores',original),('updated_radar_scores',scores)]:pd.DataFrame(arr,index=N,columns=[v.replace('\n',' ') for v in tasks]).to_csv(out/(name+'.csv'),index_label='Model')
    a=np.linspace(0,2*np.pi,8,endpoint=False);a=np.r_[a,a[0]]
    for labelled in [False,True]:
        fig,ax=plt.subplots(figsize=(14,14),subplot_kw=dict(polar=True))
        for row,n,c in zip(scores,N,C):
            v=np.r_[row,row[0]];ax.fill(a,v,color=c,alpha=.3,zorder=2);ax.plot(a,v,color='white',lw=4.5,zorder=3);ax.plot(a,v,color=c,lw=3,label=n,zorder=4)
        ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_ylim(0,10);ax.set_yticks([2,4,6,8,10]);ax.set_xticks(a[:-1]);ax.set_xticklabels(tasks if labelled else [],fontsize=17);ax.set_yticklabels(['2','4','6','8','10'] if labelled else [],fontsize=16)
        if labelled:ax.tick_params(axis='x',pad=45)
        ax.grid(color='#333333',lw=1,alpha=.7);ax.set_axisbelow(True);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.15),ncol=3,fontsize=14,edgecolor='black',facecolor='none',framealpha=1)
        fig.subplots_adjust(left=.19,right=.81,top=.84,bottom=.22);save(fig,out,'Figure7b_radar_nonI1_108'+('_labelled' if labelled else ''))
    (out/'README.md').write_text('Original radar: benchmark-data-并行/plot.ipynb cell9. SFE only updated: equal average of MAE/RMSE/MAPE ascending and R2 descending ranks; score=11-aggregate rank. This explicit rule was absent from original manual matrix. Other seven axes retain original authored scores and are not newly validated. Labelled companion identifies axes; original-style image omits axis text. Original files preserved. Run python code/update_SI_radar.py.\n',encoding='utf-8')
    print('PASS:108 pairs per model; residual-to-SFE equation checked; SI and radar exported.')
if __name__=='__main__':main()
