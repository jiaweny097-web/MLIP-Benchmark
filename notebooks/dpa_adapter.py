"""Adapter for the supplied DPA coordinates/types/cell TorchScript signature."""
import numpy as np
def build(checkpoint,device,type_map=None,dtype='float32',stress_mode='finite_difference',stress_step=1e-3):
    import torch
    from ase.calculators.calculator import Calculator,all_changes
    from benchmark_workflows import strain_matrix
    if stress_mode not in ('finite_difference','virial') or stress_step<=0:raise ValueError('Invalid DPA stress configuration.')
    class DPA(Calculator):
        implemented_properties=['energy','forces','stress']
        def __init__(self):
            super().__init__();self.network=torch.jit.load(str(checkpoint),map_location=device);self.network.eval();self.precision=getattr(torch,dtype)
            mapping=type_map
            if mapping is None and hasattr(self.network,'get_type_map'):mapping={s:i for i,s in enumerate(self.network.get_type_map())}
            if mapping is None:raise ValueError('Supply verified checkpoint type_map; atomic-number order is not assumed.')
            self.type_map=dict(mapping)
        def evaluate(self,pos,cell,symbols):
            x=torch.tensor(pos,dtype=self.precision,device=device).unsqueeze(0)
            c=torch.tensor(cell,dtype=self.precision,device=device).unsqueeze(0)
            t=torch.tensor([self.type_map[s] for s in symbols],dtype=torch.long,device=device).unsqueeze(0)
            with torch.enable_grad():return self.network(x,t,c)
        def energy(self,o):
            v=o['energy' if 'energy' in o else 'total_energy'].detach().cpu().numpy().reshape(-1)
            if len(v)!=1:raise ValueError('DPA must return one total-energy scalar.')
            return float(v[0])
        def calculate(self,atoms=None,properties=None,system_changes=all_changes):
            super().calculate(atoms,properties,system_changes)
            p=self.atoms.positions.copy();c=self.atoms.cell.array.copy();s=self.atoms.get_chemical_symbols();o=self.evaluate(p,c,s)
            self.results['energy']=self.energy(o)
            f=o['force' if 'force' in o else 'forces'].detach().cpu().numpy().reshape(-1,3)
            if f.shape!=(len(self.atoms),3):raise ValueError('Invalid force shape.')
            self.results['forces']=f.astype(float)
            if properties and 'stress' in properties:
                vol=self.atoms.get_volume()
                if vol<=0:raise ValueError('Stress needs a nonzero cell.')
                if stress_mode=='virial':
                    v=o['virial'].detach().cpu().numpy().reshape(3,3);v=-(v+v.T)/(2*vol)
                    stress=np.array([v[0,0],v[1,1],v[2,2],v[1,2],v[0,2],v[0,1]])
                else:
                    stress=np.zeros(6)
                    for j in range(6):
                        e=strain_matrix(j,stress_step);plus=np.eye(3)+e;minus=np.eye(3)-e
                        stress[j]=(self.energy(self.evaluate(p@plus.T,c@plus.T,s))-self.energy(self.evaluate(p@minus.T,c@minus.T,s)))/(2*stress_step*vol)
                self.results['stress']=stress
    return DPA()
