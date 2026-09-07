from models.biomedical_entities import DiseaseEntity

from services.sources.rxnorm_service import rxnorm_service
from services.sources.rxclass_service import rxclass_service
from services.sources.mesh_service import mesh_service


class DiseaseNormalizer:
    def normalize_compound(
        self,
        compound_name: str
    ) -> str | None:
        
        data = rxnorm_service.get_compound_rxcui(
            compound_name
        )
        
        rxnorm_ids = (
            data
            .get("idGroup", {})
            .get("rxnormId", [])
        )
        
        if not rxnorm_ids:
            return None
        
        return rxnorm_ids[0]
                
    
    
    def normalize_disease(
        self,
        rxcui: str
    ) -> list[DiseaseEntity]:
        
        response = rxclass_service.get_rxclass_info(
            rxcui
        )
                
        rxclass_info = (
            response
            .get("rxclassDrugInfoList", {})
            .get("rxclassDrugInfo", [])
        )
        
        if isinstance(rxclass_info, dict):
            rxclass_info = [rxclass_info]
            
            
        diseases = []
        seen_mesh_ids = set()
        
        for item in rxclass_info:
            disease = item.get("rxclassMinConceptItem", {})
            
            if disease.get(
                "classType"
            ) != "DISEASE":
                continue
            
            mesh_id = disease.get("classId")
            disease_name = disease.get("className")
            
            if not mesh_id or not disease_name:
                continue
            
            if mesh_id in seen_mesh_ids:
                continue
            
            mesh_descriptor = mesh_service.get_descriptor(
                mesh_id
            )

            mesh_concept_uri = mesh_descriptor.get(
                "preferredConcept"
            )
            
            if not mesh_concept_uri:
                continue
            
            mesh_concept_id = mesh_concept_uri.rsplit("/", 1)[-1]
                       
            mesh_concept_descriptor = mesh_service.get_descriptor(
                mesh_concept_id
            )            
            
            mesh_concept_scopeNote = mesh_concept_descriptor.get(
                "scopeNote", {}
            ).get("@value")
                
            diseases.append(
                DiseaseEntity(
                    mesh_id = mesh_id, 
                    mesh_concept_id = mesh_concept_id,
                    disease_name = disease_name,
                    description = mesh_concept_scopeNote
                )
            )
            
            seen_mesh_ids.add(mesh_id)        
            
        return diseases
    
    
disease_normalizer = DiseaseNormalizer()
        
        
        
        
        