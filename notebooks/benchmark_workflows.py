"""Shared future-rerun workflows; historical predictions are not rewritten."""
from pathlib import Path
import ast,csv,hashlib,importlib.metadata,io,json,platform,re,time
import numpy as np
AREA_FACTOR=16021.7733
GPA_FACTOR=160.21766208
def repo_root():
    for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents]:
        if (p/'notebooks').is_dir() and (p/'data').is_dir():return p
    raise FileNotFoundError('Run inside the published repository.')
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def dump(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    def conv(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,np.generic):return x.item()
        if isinstance(x,Path):return str(x)
        raise TypeError(type(x).__name__)
    text=json.dumps(value,default=conv,indent=2,allow_nan=False)
    temp=path.with_name(path.name+'.tmp');temp.write_text(text+'\n',encoding='utf-8');temp.replace(path)
def table(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def save_table(path,rows):
    rows=list(rows)
    if not rows:raise ValueError('No rows to save.')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def metrics(y,p):
    y=np.asarray(y,float);p=np.asarray(p,float)
    if y.shape!=p.shape or y.ndim!=1 or not len(y) or not np.isfinite(y).all() or not np.isfinite(p).all():raise ValueError('Metrics require finite paired vectors.')
    e=p-y;v=sum((y-y.mean())**2);nz=abs(y)>1e-12
    return dict(N=len(y),MAE=float(np.mean(abs(e))),RMSE=float(np.sqrt(np.mean(e**2))),R2=float(1-sum(e**2)/v) if v>0 else None,MAPE_percent=float(100*np.mean(abs(e[nz]/y[nz]))) if nz.any() else None,N_MAPE=int(nz.sum()))
def strain_matrix(j,h):
    e=np.zeros((3,3))
    if j<3:e[j,j]=h
    else:
        a,b=[(1,2),(0,2),(0,1)][j-3];e[a,b]=e[b,a]=h/2
    return e
def make_calculator(model,checkpoint,device='cpu',options=None):
    options=dict(options or {});p=Path(checkpoint).expanduser().resolve()
    if not p.is_file():raise FileNotFoundError(p)
    if model=='mace':
        from mace.calculators import MACECalculator
        return MACECalculator(model_paths=str(p),device=device,default_dtype=options.pop('default_dtype','float64'),**options)
    if model=='chgnet':
        from chgnet.model.model import CHGNet
        from chgnet.model.dynamics import CHGNetCalculator
        import inspect
        keyword='use_device' if 'use_device' in inspect.signature(CHGNetCalculator).parameters else 'device'
        return CHGNetCalculator(model=CHGNet.from_file(str(p)),**{keyword:device},**options)
    if model=='mattersim':
        from mattersim.forcefield import MatterSimCalculator
        return MatterSimCalculator(load_path=str(p),device=device,**options)
    if model=='sevennet':
        try:from sevenn.calculator import SevenNetCalculator
        except ImportError:from sevenn.sevennet_calculator import SevenNetCalculator
        return SevenNetCalculator(model=str(p),device=device,**options)
    if model=='nequip':
        try:from nequip.ase import NequIPCalculator
        except ImportError:from nequip.integrations.ase import NequIPCalculator
        return NequIPCalculator.from_compiled_model(compile_path=str(p),device=device,**options)
    if model=='dpa':
        from dpa_adapter import build
        return build(p,device,**options)
    raise ValueError(model)
def read_atoms(row,base):
    from ase import Atoms
    from ase.io import read
    if row.get('structure_path'):
        p=Path(row['structure_path']).expanduser();p=p if p.is_absolute() else Path(base)/p
        return read(str(p),index=-1)
    if row.get('poscar'):return read(io.StringIO(row['poscar']),format='vasp')
    if row.get('fractional_coords') and row.get('atom_types'):
        from ase.geometry import cellpar_to_cell
        pars=[float(row['lattice_'+s]) for s in ['a','b','c','alpha','beta','gamma']]
        return Atoms(ast.literal_eval(row['atom_types']),scaled_positions=ast.literal_eval(row['fractional_coords']),cell=cellpar_to_cell(pars),pbc=True)
    raise ValueError('Supply structure_path, inline poscar or archived bulk structure columns.')
def relax(atoms,calc,fmax=.02,max_steps=500,cell=False,mask=None):
    from ase.optimize import BFGS
    from ase.filters import FrechetCellFilter
    a=atoms.copy();a.calc=calc;initial=a.cell.array.copy();target=FrechetCellFilter(a,mask=mask) if cell else a
    opt=BFGS(target,logfile=None);ok=bool(opt.run(fmax=fmax,steps=max_steps))
    if not cell and not np.allclose(a.cell.array,initial,atol=1e-10,rtol=0):raise RuntimeError('Fixed cell changed.')
    return a,dict(converged=ok,steps=opt.nsteps,max_projected_force_eV_A=float(np.max(np.linalg.norm(a.get_forces(),axis=1))))
def snapshot(a):
    return dict(atomic_numbers=a.numbers.tolist(),positions_A=a.positions.tolist(),cell_A=a.cell.array.tolist(),pbc=a.pbc.tolist(),energy_eV=float(a.get_potential_energy()),forces_eV_A=a.get_forces(apply_constraint=False).tolist())
def static_task(a,calc,**kw):
    a=a.copy();a.calc=calc
    return dict(**snapshot(a),energy_per_atom_eV=float(a.get_potential_energy()/len(a)))
def bulk_task(a,calc,fmax=.01,max_steps=500,**kw):
    a,status=relax(a,calc,fmax,max_steps,cell=True)
    return dict(**snapshot(a),**status,lattice_parameters=a.cell.cellpar().tolist())
def vrh(c):
    if np.linalg.cond(c)>1e12:raise ValueError('Singular or ill-conditioned stiffness.')
    s=np.linalg.inv(c)
    b1=(np.trace(c[:3,:3])+2*(c[0,1]+c[0,2]+c[1,2]))/9
    g1=(np.trace(c[:3,:3])-c[0,1]-c[0,2]-c[1,2]+3*np.trace(c[3:,3:]))/15
    b2=1/(np.trace(s[:3,:3])+2*(s[0,1]+s[0,2]+s[1,2]))
    g2=15/(4*np.trace(s[:3,:3])-4*(s[0,1]+s[0,2]+s[1,2])+3*np.trace(s[3:,3:]))
    b,g=(b1+b2)/2,(g1+g2)/2
    return dict(B_VRH_GPa=float(b),G_VRH_GPa=float(g),poisson=float((3*b-2*g)/(2*(3*b+g))))
def elastic_task(a,calc,fmax=.01,max_steps=500,strain=.01,**kw):
    if not 0<strain<.05:raise ValueError('Invalid elastic strain amplitude.')
    a,status=relax(a,calc,fmax,max_steps,cell=True)
    if not status['converged']:raise RuntimeError('Equilibrium structure did not converge.')
    c=np.zeros((6,6))
    for j in range(6):
        stresses=[]
        for sign in [-1,1]:
            d=a.copy();d.set_cell(a.cell.array@(np.eye(3)+strain_matrix(j,sign*strain)).T,scale_atoms=True);d.calc=calc
            stresses.append(d.get_stress(voigt=True)*GPA_FACTOR)
        c[:,j]=(stresses[1]-stresses[0])/(2*strain)
    sym=(c+c.T)/2
    result=dict(**snapshot(a),**status,stiffness_raw_GPa=c.tolist(),stiffness_GPa=sym.tolist(),C11_GPa=float(sym[0,0]),C12_GPa=float(sym[0,1]),C44_GPa=float(sym[3,3]),minimum_stiffness_eigenvalue_GPa=float(np.linalg.eigvalsh(sym).min()),strain=strain,protocol='central engineering strain; clamped strained internal coordinates; no crystal symmetry projection')
    try:result.update(vrh(sym));result['vrh_valid']=True
    except (ValueError,ZeroDivisionError,np.linalg.LinAlgError) as e:result.update(vrh_valid=False,vrh_error=str(e))
    return result

def pair_task(row,base,calc,task,fmax,max_steps,reference_cache=None):
    a=read_atoms(dict(structure_path=row['fault_path']),base);b=read_atoms(dict(structure_path=row['perfect_path']),base)
    if not np.allclose(a.cell.array,b.cell.array,atol=1e-6,rtol=0):raise ValueError('Pair cells differ.')
    if task=='sfe':
        if sorted(a.numbers)!=sorted(b.numbers):raise ValueError('SFE pair composition mismatch.')
    else:
        from collections import Counter
        d=Counter(b.get_chemical_symbols());d.subtract(a.get_chemical_symbols());d={s:n for s,n in d.items() if n}
        if d!={row['removed_species']:1}:raise ValueError('Vacancy must remove exactly the stated species.')
    # One fixed perfect result per identical input+constraint within a run.
    bkey=hashlib.sha256(json.dumps(dict(numbers=b.numbers.tolist(),positions=b.positions.tolist(),
        cell=b.cell.array.tolist(),pbc=b.pbc.tolist(),constraints=[c.todict() for c in b.constraints]),
        sort_keys=True,default=lambda x:x.tolist() if hasattr(x,'tolist') else x).encode()).hexdigest()
    a,sa=relax(a,calc,fmax,max_steps)
    if reference_cache is not None and bkey in reference_cache:
        b,sb=reference_cache[bkey]
    else:
        b,sb=relax(b,calc,fmax,max_steps)
        if reference_cache is not None and sb['converged']:reference_cache[bkey]=(b,sb)
    ef,ep=float(a.get_potential_energy()),float(b.get_potential_energy())
    result=dict(fault=snapshot(a),perfect=snapshot(b),fault_status=sa,perfect_status=sb,converged=sa['converged'] and sb['converged'],cell_protocol='fixed; input atomic constraints preserved')
    if task=='sfe':
        area=float(np.linalg.norm(np.cross(b.cell[0],b.cell[1])));planes=int(row['fault_planes'])
        if area<=0 or planes<1:raise ValueError('Positive SFE area and fault_planes required.')
        result.update(area_A2=area,fault_planes=planes,SFE_mJ_m2=(ef-ep)/area/planes*AREA_FACTOR)
    else:
        mu=float(row['chemical_potential_eV']);result.update(vacancy_energy_eV=ef-ep+mu,removed_species=row['removed_species'],chemical_potential_eV=mu)
    return result
def surface_task(row,base,calc):
    from collections import Counter
    a=read_atoms(dict(structure_path=row['slab_path']),base);b=read_atoms(dict(structure_path=row['bulk_path']),base)
    x,y=Counter(a.get_chemical_symbols()),Counter(b.get_chemical_symbols());ratio=len(a)/len(b)
    if any(not np.isclose(x[s],ratio*y[s],atol=1e-10,rtol=0) for s in set(x)|set(y)):raise ValueError('Slab/bulk stoichiometry mismatch.')
    a.calc=b.calc=calc;area=float(np.linalg.norm(np.cross(a.cell[0],a.cell[1])));surfaces=int(row['surfaces'])
    if area<=0 or surfaces<1:raise ValueError('Positive area and explicit surface count required.')
    return dict(slab_energy_eV=float(a.get_potential_energy()),bulk_energy_per_atom_eV=float(b.get_potential_energy()/len(b)),area_A2=area,surfaces=surfaces,surface_energy_mJ_m2=float((a.get_potential_energy()-ratio*b.get_potential_energy())/area/surfaces*AREA_FACTOR),protocol='unrelaxed slab and bulk single point')
def efficiency_task(a,calc,fmax=.015,max_steps=100,**kw):
    try:
        import torch
        sync=lambda:torch.cuda.synchronize() if torch.cuda.is_available() else None
    except ImportError:sync=lambda:None
    sync();start=time.perf_counter();a,status=relax(a,calc,fmax,max_steps);sync();elapsed=time.perf_counter()-start
    return dict(**status,elapsed_s=elapsed,time_per_step_s=elapsed/status['steps'] if status['steps'] else None,final_energy_eV=float(a.get_potential_energy()),timing_scope='optimizer setup+relaxation; model initialization excluded')
def tensile_task(a,calc,axis=2,strain_step=.01,max_strain=.5,fmax=.01,max_steps=200,**kw):
    if axis not in (0,1,2) or strain_step<=0 or max_strain<0:raise ValueError('Invalid loading parameters.')
    if not np.allclose(a.cell.array,np.diag(np.diag(a.cell.array)),atol=1e-8):raise ValueError('Align loading direction with an orthogonal input axis.')
    a,status=relax(a,calc,fmax,max_steps,cell=True,mask=[True,True,True,False,False,False])
    if not status['converged']:raise RuntimeError('Initial tensile reference did not converge.')
    length=a.cell[axis,axis];previous=a.copy();rows=[];mask=[i!=axis for i in range(3)]+[False]*3
    for eps in np.arange(0,max_strain+strain_step/2,strain_step):
        d=previous.copy();box=d.cell.array.copy();box[axis,axis]=length*(1+eps);d.set_cell(box,scale_atoms=True);fixed=d.cell[axis,axis]
        d,status=relax(d,calc,fmax,max_steps,cell=True,mask=mask)
        if abs(d.cell[axis,axis]-fixed)>1e-7:raise RuntimeError('Imposed loading axis moved.')
        stress=d.get_stress()*GPA_FACTOR
        rows.append(dict(strain=float(eps),stress_xx_GPa=float(stress[0]),stress_yy_GPa=float(stress[1]),stress_zz_GPa=float(stress[2]),loading_stress_GPa=float(stress[axis]),**status))
        if not status['converged']:break
        previous=d.copy()
    return dict(axis=axis,strain_convention='engineering',stress_convention='ASE tensile-positive Cauchy stress; no automatic sign flip',curve=rows)

def versions():
    d=dict(python=platform.python_version(),platform=platform.platform())
    for pkg in ['ase','numpy','torch','mace-torch','chgnet','nequip','sevenn','mattersim']:
        try:d[pkg]=importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:pass
    return d
def run_task(task,manifest,output,calculator,parameters=None,model_identity=None):
    manifest=Path(manifest).resolve();output=Path(output).resolve();rows=table(manifest);params=dict(parameters or {})
    if model_identity is None:raise ValueError('Pass explicit model_identity with checkpoint hash for reproducible runs.')
    ids=[str(r.get('ID') or r.get('material_id') or '') for r in rows]
    if not rows or len(set(ids))!=len(ids) or any(not re.fullmatch(r'[A-Za-z0-9_.-]+',s) or s in ('.','..') for s in ids):raise ValueError('Require nonempty unique safe IDs.')
    if task not in ['static','bulk','elastic','vacancy','sfe','surface','efficiency','tensile']:raise ValueError(task)
    if task=='sfe' and any(r.get('fault_type') not in ['I1','I2','ISF','ESF'] for r in rows):raise ValueError('Explicit SFE fault_type required.')
    files={}
    for r in rows:
        for k in ['structure_path','fault_path','perfect_path','slab_path','bulk_path']:
            if r.get(k):
                p=Path(r[k]).expanduser();p=p if p.is_absolute() else manifest.parent/p;files[str(p.resolve())]=sha(p)
    signature=hashlib.sha256(json.dumps(dict(task=task,manifest=sha(manifest),parameters=params,input_files=files,model_identity=model_identity,workflow_sha256=sha(__file__)),sort_keys=True).encode()).hexdigest()
    output.mkdir(parents=True,exist_ok=True);recorddir=output/'records';recorddir.mkdir(exist_ok=True)
    if (output/'run.json').exists():
        if json.loads((output/'run.json').read_text())['signature']!=signature:raise ValueError('Incompatible resume: use a fresh output directory.')
    else:dump(output/'run.json',dict(signature=signature,task=task,parameters=params,model_identity=model_identity,versions=versions()))
    results=[];failures=[];reference_cache={}
    for ID,row in zip(ids,rows):
        dest=recorddir/(ID+'.json')
        if dest.exists():
            r=json.loads(dest.read_text())
            if r['run_signature']!=signature:raise ValueError('Mismatched record signature.')
            if r.get('converged',True) and task not in ('sfe','vacancy'):
                results.append(r);print(f'Reusing {task}: {ID}');continue
            print(f'Retrying nonconverged sample: {ID}')
        print(f'Running {task}: {ID}')
        try:
            if task in ('sfe','vacancy'):r=pair_task(row,manifest.parent,calculator,task,params.get('fmax',.02 if task=='sfe' else .027),params.get('max_steps',500),reference_cache=reference_cache)
            elif task=='surface':r=surface_task(row,manifest.parent,calculator)
            else:
                fn=dict(static=static_task,bulk=bulk_task,elastic=elastic_task,efficiency=efficiency_task,tensile=tensile_task)[task];r=fn(read_atoms(row,manifest.parent),calculator,**params)
            r=dict(ID=ID,run_signature=signature,task=task,**r);dump(dest,r);results.append(r)
        except Exception as e:
            failures.append(dict(ID=ID,error_type=type(e).__name__,error=str(e)));print(f'FAILED {ID}: {type(e).__name__}: {e}')
    dump(output/'failures.json',failures);dump(output/'results.json',results)
    if failures:raise RuntimeError(f'{len(failures)} failed samples; inspect failures.json.')
    return results
