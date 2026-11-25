"""Plot the archived tensile curves as a publication-style 2-by-2 figure."""
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code' / 'reproduce'))
from tensile_original_metrics import read_archived_curve, get_peak

MODELS = ['nequip', 'mace', 'sevennet', 'dpa', 'chgnet', 'mattersim']
LABELS = ['NequIP', 'MACE', 'SevenNet', 'DPA-3-FT', 'CHGNet', 'MatterSim']
COLORS = ['#F3891C', '#F8AD63', '#FDE1C7', '#4874CB', '#A1BEE4', '#E0E7FF']


def main():
    plt.rcParams.update({'font.family': 'Arial', 'font.size': 15,
                         'axes.linewidth': 1.1, 'svg.fonttype': 'none',
                         'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 10.3))
    limits = {'Mo': (15, (-15, 31)), 'W': (48, (-15.5, 33.5)),
              'Cu': (48, (-1.2, 26.3)), 'Al': (50, (-0.7, 15.3))}
    for ax, element in zip(axes.flat, limits):
        xmax, ylim = limits[element]
        for model, color in zip(MODELS, COLORS):
            x, y = read_archived_curve(model, element)
            x = x * 100
            visible = (x >= 0) & (x <= xmax + 1e-9)
            vx, vy = x[visible], y[visible]
            if len(vx) and vx[-1] < xmax and x.min() <= xmax <= x.max():
                vx = np.append(vx, xmax)
                vy = np.append(vy, np.interp(xmax, x, y))
            ax.plot(vx, vy, color=color, linewidth=2.2)
            _, px, py = get_peak(x, y, element)
            if 0 <= px <= xmax:
                ax.scatter(px, py, s=65, facecolors=color,
                           edgecolors='#666666', linewidths=1.0, zorder=5)
        x, y = read_archived_curve('dft', element)
        ax.plot(x * 100, y, color='black', linestyle='--', linewidth=1.3)
        _, px, py = get_peak(x, y, element)
        ax.scatter(px * 100, py, marker='*', s=180, c='black',
                   edgecolors='white', linewidths=0.7, zorder=6)
        ax.axhline(0, color='0.5', linestyle=':', linewidth=1)
        ax.set(xlim=(0, xmax), ylim=ylim)
        ax.xaxis.set_major_locator(MultipleLocator(2.5 if element == 'Mo' else 10))
        ax.yaxis.set_major_locator(MultipleLocator(2.5 if element == 'Al' else 5 if element == 'Cu' else 10))
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.tick_params(which='major', length=5, width=1)
        ax.tick_params(which='minor', length=2.5, width=0.8)
    for ax in axes[:, 0]:
        ax.set_ylabel(r'Tensile Stress $\sigma_{zz}$ (GPa)', fontsize=18)
    for ax in axes[1, :]:
        ax.set_xlabel('Strain (%)', fontsize=18)
    handles = [Line2D([], [], color=c, linewidth=2.2, label=n)
               for c, n in zip(COLORS, LABELS)]
    handles.append(Line2D([], [], color='black', linestyle='--',
                          linewidth=1.3, label='DFT (Ref.)'))
    fig.legend(handles=handles, loc='lower center', ncol=4, frameon=False,
               title='Machine Learning Potentials', title_fontsize=18,
               fontsize=16, handlelength=2.6, columnspacing=1.3,
               bbox_to_anchor=(0.52, 0.005))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.985,
                        bottom=0.19, wspace=0.18, hspace=0.24)
    out = ROOT / 'results' / 'tensile'
    out.mkdir(parents=True, exist_ok=True)
    for extension in ['jpg']:
        path = out / ('Fig6_combined_sigmaZZ.' + extension)
        fig.savefig(path, dpi=400, facecolor='white')
        print(path)
    plt.close(fig)


if __name__ == '__main__':
    main()
