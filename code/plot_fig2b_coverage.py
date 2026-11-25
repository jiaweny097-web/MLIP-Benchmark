"""Replot element coverage from explicit per-case rows; count presence, not atoms."""
from pathlib import Path
from collections import Counter
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

ROOT=Path(__file__).resolve().parents[1]
layout=[
    'H . . . . . . . . . . . . . . . . He',
    'Li Be . . . . . . . . . . B C N O F Ne',
    'Na Mg . . . . . . . . . . Al Si P S Cl Ar',
    'K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr',
    'Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe',
    'Cs Ba * Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn',
    'Fr Ra * Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og']
coords={e:(group,period) for period,row in enumerate(layout,1) for group,e in enumerate(row.split(),1) if e not in ['.','*']}
coords.update({e:(i+3,8.5) for i,e in enumerate('La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu'.split())})
coords.update({e:(i+3,9.5) for i,e in enumerate('Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr'.split())})
# Match the original Element.is_metal convention: metalloids are not coloured.
nonmetals=set('H He B C N O F Ne Si P S Cl Ar Ge As Se Br Kr Sb Te I Xe Po At Rn Ts Og'.split())
metals=set(coords)-nonmetals

def main():
    out=ROOT/'analysis/fig2b'
    source=pd.read_csv(out/'coverage_source_rows.csv',dtype=str)
    source=source[source.scope=='release_reference_scope']
    out=ROOT/'results/fig2b';out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'Arial','font.weight':'normal','axes.labelweight':'normal','svg.fonttype':'none','pdf.fonttype':42})
    all_counts=[]
    cmap=LinearSegmentedColormap.from_list('DeepBlueToOrange',['#4874CB','#A5C1E5','#F8F9FA','#FFD9B7','#F3891C'])
    for scope,df in source.groupby('scope',sort=False):
        counts=Counter();tasks={}
        for _,r in df.iterrows():
            elements=set(re.findall(r'[A-Z][a-z]?',r.formula))
            assert 'Po' not in elements, r.to_dict()
            present=elements&metals
            counts.update(present)
            tasks.setdefault(r.task,Counter()).update(present)
        for el in sorted(coords):all_counts.append(dict(scope=scope,element=el,case_count=counts[el],**{t:c[el] for t,c in tasks.items()}))
        fig=plt.figure(figsize=(14,6.8))
        ax=fig.add_axes([.05,.05,.9,.68]);ax.set_aspect('equal')
        lo,hi=min(counts.values()),max(counts.values());norm=Normalize(lo,hi)
        for e,(group,period) in coords.items():
            count=counts[e];v=norm(count) if count else .5
            fill=cmap(v) if count else '#F2F2F2'
            color=('white' if v<.15 or v>.85 else 'black') if count else '#888888'
            ax.add_patch(plt.Rectangle((group,-period),1,1,facecolor=fill,edgecolor='black',linewidth=.5 if count else .3))
            ax.text(group+.5,-period+.5,e,ha='center',va='center',color=color,fontsize=12,fontweight='normal')
        for period,label in [(6,'La–Lu'),(7,'Ac–Lr')]:
            ax.add_patch(plt.Rectangle((3,-period),1,1,facecolor='#F2F2F2',edgecolor='black',linewidth=.3))
            ax.text(3.5,-period+.5,label,ha='center',va='center',fontsize=9,color='#888888',fontweight='normal')
        ax.set(xlim=(.5,19.5),ylim=(-10.5,.5));ax.axis('off')
        cax=fig.add_axes([.35,.75,.3,.02])
        cax.imshow(np.linspace(0,1,256).reshape(1,-1),aspect='auto',cmap=cmap)
        cax.set_yticks([]);cax.set_xticks([0,128,255],[str(lo),str((lo+hi)//2),str(hi)],fontsize=12,fontweight='normal')
        cax.xaxis.set_label_position('top');cax.set_xlabel('Element Counts',fontsize=13,fontweight='normal',labelpad=10)
        for spine in cax.spines.values():spine.set_visible(False)
        for ext in ['jpg']:fig.savefig(out/f'Fig2b_elements_{scope}.{ext}',dpi=350,bbox_inches='tight',transparent=True)
        plt.close(fig)
        print(scope,'cases=',len(df),'metal species=',len(counts),'counts=',dict(counts))
    pd.DataFrame(all_counts).fillna(0).to_csv(out/'element_counts.csv',index=False)

if __name__=='__main__':main()
