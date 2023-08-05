# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.04.10
version: 2023.04.10
function: Some small tools for scholar
"""
import re
import ase.io
from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor


class StructureCif():
    """
    """
    def __init__(self, file):
        self.file = file
        self.type = 'cif' if self.file.endswith('cif') else 'poscar'
        
        self.atoms = self.get_ase_atoms()
        self.oxi_states = self.get_oxi_states()
        
        self.structure = self.get_pmg_stru_from_atoms()
        self.stru = self.structure
    
    def get_ase_atoms(self):
        if self.type == 'cif':
            return ase.io.read(self.file, format='cif', store_tags=True)
        elif self.type == 'poscar':
            return ase.io.read(self.file, format='vasp')
    
    def get_oxi_states(self):
        """Require atoms read from cif with oxi states"""
        symbols = self.atoms.info['_atom_type_symbol']
        symbols = [ re.findall('[A-Z][a-z]*', i)[0] for i in symbols]
        oxis = self.atoms.info['_atom_type_oxidation_number']
        oxi_states = {s: o for s, o in zip(symbols, oxis)}
        return oxi_states
    
    def get_pmg_stru(self):
        try:
            stru = Structure.from_file(self.file)
        except:
            stru = AseAtomsAdaptor.get_structure(self.atoms)
            stru.add_oxidation_state_by_element(self.oxi_states)
        return stru
    
    def get_pmg_stru_from_atoms(self):
        stru = AseAtomsAdaptor.get_structure(self.atoms)
        stru.add_oxidation_state_by_element(self.oxi_states)
        return stru
        
        
        