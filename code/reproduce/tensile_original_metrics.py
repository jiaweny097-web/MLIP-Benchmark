from pathlib import Path
import pickle
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
ELASTIC_LIMIT = 0.05
MODELS = dict(dpa='DPA', nequip='NequIP', sevennet='SevenNet', chgnet='CHGNet', mace='MACE', mattersim='MatterSim')
def read_archived_curve(role, element):
    path=ROOT/'data/tensile'/('dft/reference.pkl' if role=='dft' else 'predictions/'+role+'.pkl')
    with path.open('rb') as f: records=pickle.load(f)['records']
    row=next(r for r in records if r['ID']==element)
    df=pd.DataFrame(row['curve'])[['strain','stress_zz_gpa']].apply(pd.to_numeric,errors='coerce').dropna()
    if len(df)<2: raise ValueError('Insufficient curve points')
    v=df['strain'].to_numpy()
    df['strain']=v/100 if np.nanmax(abs(v))>1.5 else v
    df=df.groupby('strain',as_index=False)['stress_zz_gpa'].mean()
    return df.strain.to_numpy(),df.stress_zz_gpa.to_numpy()
def get_peak(strain, stress, element):
    """用向量化查找代替手写循环"""
    if strain is None or len(strain) == 0:
        return (None, None, None)
    if element == 'W':
        descending = np.where(np.diff(stress) < 0)[0]
        peak_idx = descending[0] if len(descending) > 0 else len(stress) - 1
    else:
        peak_idx = np.argmax(stress)
    return (peak_idx, strain[peak_idx], stress[peak_idx])

def percent_error(pred, ref):
    return np.nan if ref is None or np.isnan(ref) or abs(ref) < 1e-12 else abs(pred - ref) / abs(ref) * 100.0

def trapz_integral(y, x):
    return getattr(np, 'trapezoid', np.trapz)(y, x)

def compute_metrics_for_one_model(ele, folder, model_key):
    dft_strain, dft_stress = read_archived_curve('dft', ele)
    ml_strain, ml_stress = read_archived_curve(model_key, ele)
    if dft_strain is None or ml_strain is None:
        return None
    _, dft_peak_strain, dft_peak_stress = get_peak(dft_strain, dft_stress, ele)
    _, ml_peak_strain, ml_peak_stress = get_peak(ml_strain, ml_stress, ele)
    if dft_peak_strain is None or ml_peak_strain is None:
        return None
    eval_min, eval_max = (max(0.0, dft_strain.min(), ml_strain.min()), min(dft_peak_strain, dft_strain.max(), ml_strain.max()))
    mask = (dft_strain >= eval_min) & (dft_strain <= eval_max)
    eps_eval, dft_eval = (dft_strain[mask], dft_stress[mask])
    if len(eps_eval) < 2:
        return None
    ml_eval = np.interp(eps_eval, ml_strain, ml_stress)
    elastic_mask = eps_eval <= ELASTIC_LIMIT
    if elastic_mask.sum() >= 2:
        eps_el, dft_el, ml_el = (eps_eval[elastic_mask], dft_eval[elastic_mask], ml_eval[elastic_mask])
        E_dft, E_ml = (np.polyfit(eps_el, dft_el, 1)[0], np.polyfit(eps_el, ml_el, 1)[0])
        E001_rel_error, MAE_elastic = (percent_error(E_ml, E_dft), np.mean(np.abs(ml_el - dft_el)))
    else:
        E_dft = E_ml = E001_rel_error = MAE_elastic = np.nan
    IASE = trapz_integral(np.abs(ml_eval - dft_eval), eps_eval)
    DFT_abs_area = trapz_integral(np.abs(dft_eval), eps_eval)
    NIASE = IASE / DFT_abs_area * 100.0 if abs(DFT_abs_area) > 1e-12 else np.nan
    U_dft, U_ml = (trapz_integral(dft_eval, eps_eval), trapz_integral(ml_eval, eps_eval))
    strain_energy_abs = abs(U_ml - U_dft)
    strain_energy_rel = strain_energy_abs / abs(U_dft) * 100.0 if abs(U_dft) > 1e-12 else np.nan
    return {'Element': ele, 'Model': MODELS[model_key], 'Model_key': model_key, 'DFT_peak_strain_%': dft_peak_strain * 100.0, 'DFT_peak_stress_GPa': dft_peak_stress, 'ML_peak_strain_%': ml_peak_strain * 100.0, 'ML_peak_stress_GPa': ml_peak_stress, 'E001_DFT_GPa': E_dft, 'E001_ML_GPa': E_ml, 'E001_relative_error_%': E001_rel_error, 'MAE_elastic_GPa': MAE_elastic, 'IASE_GPa': IASE, 'NIASE_%': NIASE, 'Strain_energy_DFT_GPa': U_dft, 'Strain_energy_ML_GPa': U_ml, 'Strain_energy_abs_error_GPa': strain_energy_abs, 'Strain_energy_relative_error_%': strain_energy_rel, 'Peak_stress_abs_error_GPa': abs(ml_peak_stress - dft_peak_stress), 'Peak_stress_relative_error_%': percent_error(ml_peak_stress, dft_peak_stress), 'Peak_strain_abs_error_%strain': abs(ml_peak_strain - dft_peak_strain) * 100.0, 'Peak_strain_relative_error_%': percent_error(ml_peak_strain, dft_peak_strain), 'Evaluation_max_strain_%': eval_max * 100.0, 'Coverage_to_DFT_peak_%': eval_max / dft_peak_strain * 100.0 if abs(dft_peak_strain) > 1e-12 else np.nan}
