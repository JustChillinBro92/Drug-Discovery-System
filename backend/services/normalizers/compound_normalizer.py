import re

from models.biomedical_entities import CompoundEntity
from services.sources.chembl_service import chembl_service


class CompoundNormalizer:

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Normalize a compound name for exact comparison.
        """
        name = name.lower().strip()
        name = re.sub(r"[^a-z0-9]+", " ", name)
        return " ".join(name.split())



    def _find_best_match(
        self,
        compound_name: str,
        molecules: list[dict]
    ) -> tuple[dict, float]:

        query = self._normalize_name(compound_name)

        # 1. Exact preferred-name match
        for molecule in molecules:
            pref_name = molecule.get("pref_name")

            if (
                pref_name
                and self._normalize_name(pref_name) == query
            ):
                return molecule, 1.0

        # 2. Exact synonym match
        for molecule in molecules:
            for synonym in molecule.get(
                "molecule_synonyms",
                []
            ):
                molecule_synonym = synonym.get(
                    "molecule_synonym"
                )
                
                synonyms_value = synonym.get(
                    "synonyms"
                )

                if (
                    molecule_synonym
                    and self._normalize_name(
                        molecule_synonym
                    ) == query
                ):
                    return molecule, 0.95

                if (
                    synonyms_value
                    and self._normalize_name(
                        synonyms_value
                    ) == query
                ):
                    return molecule, 0.95


        # 3. Fallback to ChEMBL search score
        best_match = max(
            molecules,
            key=lambda molecule: molecule.get(
                "score",
                float("-inf")
            )
        )

        return best_match, 0.5


    def normalize(
        self,
        compound_name: str
    ) -> CompoundEntity:

        # 1. Search ChEMBL
        search_result = chembl_service.search_compound(
            compound_name
        )

        molecules = search_result.get(
            "molecules",
            []
        )

        if not molecules:
            raise Exception(
                f"No compound found for {compound_name}"
            )

        # 2. Find the actual best match
        best_match, confidence = self._find_best_match(
            compound_name,
            molecules
        )

        # 3. Get ChEMBL ID
        chembl_id = best_match.get(
            "molecule_chembl_id"
        )

        if not chembl_id:
            raise Exception(
                "ChEMBL ID not found"
            )

        # 4. Get complete molecule details
        molecule = chembl_service.get_molecule(
            chembl_id
        )

        # 5. Extract structure information
        structures = (
            molecule.get(
                "molecule_structures",
                {}
            )
            or {}
        )

        properties = (
            molecule.get(
                "molecule_properties",
                {}
            )
            or {}
        )

        smiles = structures.get(
            "canonical_smiles"
        )

        inchikey = structures.get(
            "standard_inchi_key"
        )

        formula = properties.get(
            "full_molformula"
        )

        # 6. Canonical name
        canonical_name = (
            molecule.get("pref_name")
            or compound_name.upper()
        )

        # 7. Safety check
        if not smiles:
            raise Exception(
                f"No SMILES found for {compound_name}"
            )

        # 8. Return normalized entity
        return CompoundEntity(
            original_text=compound_name,
            canonical_name=canonical_name,
            confidence=confidence,
            chembl_id=chembl_id,
            smiles=smiles,
            inchikey=inchikey,
            molecular_formula=formula
        )


compound_normalizer = CompoundNormalizer()