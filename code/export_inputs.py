"""Export actual retained input structures/manifests without loading any model."""
from pathlib import Path
import argparse,csv,hashlib,io,json,pickle,re
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def load(rel):
    with (ROOT/'data'/rel).open('rb') as f:return pickle.load(f)['records']

def atoms_from_record(s):
    from ase import Atoms
    from ase.geometry import cellpar_to_cell
    from ase.constraints import FixAtoms,FixCartesian,FixScaled
    cell=s.get('cell_A')
    if cell is None:cell=cellpar_to_cell(s['cell_parameters'])
    atom_args={'symbols':s['symbols']} if 'symbols' in s else {'numbers':s['atomic_numbers']}
    if 'fractional_positions' in s:atom_args['scaled_positions']=s['fractional_positions']
    else:atom_args['positions']=s['positions_A']
    a=Atoms(**atom_args,cell=cell,pbc=s.get('pbc',[True]*3))
    constraints=[]
    # POSCAR flags are movable=True. ASE masks are fixed=True.
    flags=s.get('movement_flags',s.get('selective_dynamics'))
    if flags is not None:
        for i,row in enumerate(flags):
            moving=[(v.upper()=='T') if isinstance(v,str) else bool(v) for v in row]
            if not all(moving):constraints.append(FixScaled(i,mask=np.logical_not(moving)))
    for c in s.get('constraints',[]):
        name=c.get('type',c.get('name'));state=c.get('state',c.get('kwargs',{}))
        index=state.get('index',state.get('indices',state.get('a')))
        if name=='FixAtoms':constraints.append(FixAtoms(indices=index))
        elif name in ['FixCartesian','FixScaled']:
            cls=FixCartesian if name=='FixCartesian' else FixScaled
            constraints.append(cls(index,mask=state['mask']))
        else:raise ValueError('Unsupported saved constraint: '+str(c))
    a.set_constraint(constraints)
    for name,values in s.get('per_atom_arrays',{}).items():
        if name=='initial_magmoms':a.set_initial_magnetic_moments(values)
        elif name=='initial_charges':a.set_initial_charges(values)
    return a

def main():
    from ase.io import read,write
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'inputs')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    structures=out/'structures';structures.mkdir(exist_ok=True)
    provenance=[];manifests={};cache={}
    def export(s,label,text=None,fmt=None):
        a=read(io.StringIO(text),format=fmt) if text is not None else atoms_from_record(s)
        # ASE JSON preserves PBC, atom order, constraints and per-atom state.
        source_identity=json.dumps(dict(numbers=a.numbers.tolist(),positions=a.positions.tolist(),cell=a.cell.array.tolist(),pbc=a.pbc.tolist(),constraints=[c.todict() for c in a.constraints],magmoms=a.get_initial_magnetic_moments().tolist()),sort_keys=True,default=lambda x:x.tolist()).encode()
        digest=hashlib.sha256(source_identity).hexdigest()
        if digest not in cache:
            path=structures/(digest+'.json')
            if not path.exists():write(path,a,format='json')
            b=read(path);assert np.array_equal(a.numbers,b.numbers)
            np.testing.assert_allclose(a.positions,b.positions,atol=1e-12)
            np.testing.assert_allclose(a.cell.array,b.cell.array,atol=1e-12)
            assert np.array_equal(a.pbc,b.pbc)
            def signature(v):return json.dumps([c.todict() for c in v.constraints],sort_keys=True,default=lambda x:x.tolist())
            assert signature(a)==signature(b)
            cache[digest]=path.relative_to(out).as_posix()
        provenance.append(dict(source=label,structure_path=cache[digest],structure_sha256=digest,N_atoms=len(a)))
        return cache[digest]
    def table(name,rows):
        assert rows and len({r['ID'] for r in rows})==len(rows),name
        with (out/(name+'.csv')).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        manifests[name]=len(rows)
    bulk=[]
    for r in load('bulk_elastic/dft/reference.pkl'):
        bulk.append(dict(ID=r['ID'],structure_path=export(r['structure'],'bulk_elastic/'+r['ID'])))
    for name in ['bulk','elastic','static_bulk']:table(name,bulk)
    # Default STATIC_MANIFEST in existing six model notebooks is static.csv.
    table('static',bulk)
    table('static_vacancy',[dict(ID=f'{i+1:03d}',structure_path=export(r['atoms'],'static_vacancy/'+r['filename'])) for i,r in enumerate(load('static calculation/static_vacancy/dft/snapshots.pkl'))])
    vacancy=[]
    for r in load('vacancy/dft/reference.pkl'):
        vacancy.append(dict(ID=r['ID'],fault_path=export(r['vacancy_input'],'vacancy/'+r['ID']+'/fault'),perfect_path=export(r['perfect_input'],'vacancy/'+r['ID']+'/perfect'),removed_species=r['removed_species'],chemical_potential_eV=r['chemical_potential_eV']))
    table('vacancy',vacancy)
    with (ROOT/'data/sfe_nonI1/paired_model_results.csv').open(encoding='utf-8',newline='') as stream:
        active={r['pair_key'] for r in csv.DictReader(stream) if r['six_model_common'].lower()=='true' and r['previous_author_exclusion'].lower()!='true'}
    sfe=[]
    for r in load('sfe_nonI1/reference.pkl'):
        if r['pair_key'] not in active:continue
        sfe.append(dict(ID=r['ID'],fault_path=export(None,r['pair_key']+'/fault',r['fault_POSCAR_text'],'vasp'),perfect_path=export(None,r['pair_key']+'/perfect',r['perfect_POSCAR_text'],'vasp'),fault_type=r['fault_type'].upper(),fault_planes=1))
    table('sfe',sfe);assert len(sfe)==108
    bulks={r['mpid']:r for r in load('surface/dft/bulk_structures.pkl')};surface=[]
    for r in load('surface/dft/reference.pkl'):
        match=re.search(r'mp-\d+',r['ID']);assert match,r['ID'];b=bulks[match.group()]
        surface.append(dict(ID=r['ID'],slab_path=export(r['structure'],'surface/'+r['ID']),bulk_path=export(b['atoms'],'surface_bulk/'+b['mpid']),surfaces=2))
    table('surface',surface)
    table('efficiency',[dict(ID=r['ID'],structure_path=export(r['structure'],'efficiency/'+r['ID'])) for r in load('efficiency/inputs/structures.pkl')])
    table('tensile',[dict(ID=r['ID'],structure_path=export(None,'tensile/'+r['ID'],r['structure_text'],r['structure_format'])) for r in load('tensile/dft/reference.pkl')])
    with (out/'provenance.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(provenance[0]));w.writeheader();w.writerows(provenance)
    (out/'summary.json').write_text(json.dumps(dict(manifests=manifests,unique_structures=len(cache),scope='actual retained input structures; cleaned workflows may differ from historical optimizer settings; no model inference performed',static_vacancy='archived snapshot inputs; not formation-energy relaxed states',surface='unrelaxed slab and associated bulk',sfe='108 non-I1/non-Po pairs excluding MgCa I2'),indent=2),encoding='utf-8')
    print(json.dumps(dict(manifests=manifests,unique_structures=len(cache))))

if __name__=='__main__':main()
