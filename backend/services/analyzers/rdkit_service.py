from rdkit import Chem
from rdkit.Chem import (
    Crippen, 
    Descriptors,
    Lipinski,
    QED,
    rdMolDescriptors
)

from models.biomedical_entities import CompoundEntity
from models.molecular_properties import (
    LipinskiResult,
    MolecularProperties
)


class RDKitService:
    # Checks whether compound contains a valid SMILES representation
    
    def validate_compound(self, compound: CompoundEntity) -> bool:
        molecule = Chem.MolFromSmiles(compound.smiles) 
        
        return molecule is not None
    
    
    # Calculate molecular descriptors & evaluate Lipinski's Rule of Five using RDKit.
    
    def analyze_properties(self, compound: CompoundEntity) -> MolecularProperties:
        molecule = Chem.MolFromSmiles(compound.smiles)
        
        if molecule is None:
            raise ValueError(f"Invalid SMILES for compound: {compound.canonical_name}")
        
        # Molecular Descriptors
        
        molecular_weight = Descriptors.MolWt(molecule)
        logp = Crippen.MolLogP(molecule)
        tpsa = rdMolDescriptors.CalcTPSA(molecule)
        h_bond_donors = Lipinski.NumHDonors(molecule)
        h_bond_acceptors = Lipinski.NumHAcceptors(molecule)
        rotatable_bonds = Lipinski.NumRotatableBonds(molecule)
        heavy_atom_count = Lipinski.HeavyAtomCount(molecule)
        ring_count = Lipinski.RingCount(molecule)
        aromatic_ring_count = Lipinski.NumAromaticRings(molecule)
        formal_charge = Chem.GetFormalCharge(molecule)
        fraction_csp3 = Lipinski.FractionCSP3(molecule)
        qed = QED.qed(molecule)
        
        # Lipinski Rule of Five
        
        molecular_weight_pass = molecular_weight <= 500
        logp_pass = logp <= 5
        hbd_pass = h_bond_donors <= 5
        hba_pass = h_bond_acceptors <= 10
        
        violations = 0
        
        if not molecular_weight_pass:
            violations += 1
        if not logp_pass:
            violations += 1
        if not hbd_pass:
            violations += 1
        if not hba_pass:
            violations += 1

        # Atmost 1 violation allowed
        overall_pass = violations <= 1
        
        lipinski = LipinskiResult(
            molecular_weight_pass=molecular_weight_pass,
            logp_pass=logp_pass,
            hbd_pass=hbd_pass,
            hba_pass=hba_pass,
            overall_pass=overall_pass,
            violations=violations
        )
        
        # Return the molecular description
        
        return MolecularProperties(
            molecular_weight=molecular_weight,
            logp=logp,
            tpsa=tpsa,
            h_bond_donors=h_bond_donors,
            h_bond_acceptors=h_bond_acceptors,
            rotatable_bonds=rotatable_bonds,
            heavy_atom_count=heavy_atom_count,
            ring_count=ring_count,
            aromatic_ring_count=aromatic_ring_count,
            formal_charge=formal_charge,
            fraction_csp3=fraction_csp3,
            qed=qed,
            lipinski=lipinski
        )
        
        
rdkit_service = RDKitService()