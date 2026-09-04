from services.sources.unichem_service import unichem_service


class UniChemNormalizer:
    PUBCHEM_SOURCE_ID = 22

    def normalize(
        self,
        chembl_id: str,
    ) -> dict:
        
        compound_sources = unichem_service.get_compound_sources(
            chembl_id
        )
        
        compounds = compound_sources.get("compounds", [])
        if not compounds:
            raise Exception(f"No compound found for {chembl_id}")


        sources = compounds[0].get("sources", [])
        
        pubchem_cids = [
            source.get("compoundId")
            for source in sources
            if (
                source.get("id") == self.PUBCHEM_SOURCE_ID
                and source.get("compoundId") is not None
            )
        ]

        if not pubchem_cids:
            raise Exception(f"No PubChem compound found for {chembl_id}")
        
        return {
            "chembl_id": chembl_id,
            "pubchem_cids": pubchem_cids
        }
        
        
unichem_normalizer = UniChemNormalizer()