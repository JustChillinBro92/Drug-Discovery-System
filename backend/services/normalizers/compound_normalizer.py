from models.biomedical_entities import CompoundEntity

from services.sources.chembl_service import chembl_service

# from services.normalizers.synonym_cleaner import synonym_cleaner


class CompoundNormalizer:
    def normalize(
        self, 
        compound_name: str
    ) -> CompoundEntity:
        # 1: search up the compound & its similarities using ChEMBL service
        
        search_result = chembl_service.search_compound(compound_name)
        
        molecules = search_result.get("molecules", [])
        if not molecules:
            raise Exception(f"No compound found for {compound_name}")
        
        
        # 2: Pick up the best matching compound & get its ChEMBL id
        
        best_match = molecules[0]
        chembl_id = best_match["molecule_chembl_id"]
        
        if not chembl_id:
            raise Exception("ChEMBL ID not found")
        
            
        # 3: Get the details of the best match using ChEMBL service
        
        molecule = chembl_service.get_molecule(chembl_id)
        
        
        # 4: Extract the structure information
        
        structures = molecule.get("molecule_structures", {}) or {}
        properties = molecule.get("molecule_properties", {}) or {}
        
        
        # 5: Extract synonyms
        
        # raw_synonyms = []
        
        # for synonym in molecule.get(
        #     "molecule_synonyms", []
        # ):
        #     name = synonym.get("molecule_synonym")
        #     if name:
        #         raw_synonyms.append(name)
        
        
        # synonyms = synonym_cleaner.clean(raw_synonyms)

        
        # 6: Extract chemical data safely

        smiles = None

        if structures:
            smiles = structures.get("canonical_smiles")
            
        inchikey = structures.get("standard_inchi_key")
        formula = properties.get("full_molformula")
        
        canonical_name = (
            molecule.get("pref_name")
            or compound_name.upper()
        )

        
        # Safety checks

        if not smiles:
            raise Exception(f"No SMILES found for {compound_name}")

        
        # 7: Return the final normalized entity
        
        return CompoundEntity(
            original_text = compound_name,
            canonical_name = canonical_name,
            confidence = 1.0,
            # synonyms = synonyms,
            chembl_id = chembl_id,
            smiles = smiles,
            inchikey = inchikey,
            molecular_formula = formula            
        )
        
        
compound_normalizer = CompoundNormalizer()
        
    