from config.config import settings

from models.biomedical_entities import (
    CompoundEntity,
    ProteinEntity,
    DiseaseEntity,
    SideEffectEntity,
    PathwayEntity,
    DockingResultEntity
)
from models.compound_analysis import CompoundAnalysis

from models.paper_entity import PaperEntity

from .neo4j_client import Neo4jClient
from . import graph_queries


class GraphService:

    def __init__(
        self,
        uri: str,
        username: str,
        password: str
    ):

        self.client = Neo4jClient(
            uri=uri,
            username=username,
            password=password
        )
        
        self.client.initialize_schema()


    def close(self):
        self.client.close()


    # |=================================|
    # | CREATE & ADD THE GRAPH NODES    |
    # |=================================|


    # ========================================================
    # Compound
    # ========================================================

    def add_compound(
        self,
        compound: CompoundAnalysis
    ):
        params = {
            **compound.compound.model_dump(),
            **compound.properties.model_dump(exclude={"lipinski"}),
            **{
                f"lipinski_{key}": value
                for key, value in compound.properties.lipinski.model_dump().items()
            }
        }

        self.client.execute_query(
            graph_queries.ADD_COMPOUND,
            params
        )


    # ========================================================
    # Protein
    # ========================================================

    def add_protein(
        self,
        protein: ProteinEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_PROTEIN,
            protein.model_dump()
        )


    # ========================================================
    # Disease
    # ========================================================

    def add_disease(
        self,
        disease: DiseaseEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_DISEASE,
            disease.model_dump()
        )


    # ========================================================
    # Side Effect
    # ========================================================

    def add_side_effect(
        self,
        side_effect: SideEffectEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_SIDE_EFFECT,
            side_effect.model_dump()
        )


    # ========================================================
    # Pathway
    # ========================================================

    def add_pathway(
        self,
        pathway: PathwayEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_PATHWAY,
            pathway.model_dump()
        )


    # ========================================================
    # Paper
    # ========================================================

    def add_paper(
        self,
        paper: PaperEntity
        ):

        paper_id = (
            paper.pmid
            or paper.pmcid
            or paper.doi
        )

        if not paper_id:
            raise ValueError(
                "Paper must have PMID, PMCID, or DOI."
            )

        self.client.execute_query(
            graph_queries.ADD_PAPER,
            {
                "paper_id": paper_id,
                "pmid": paper.pmid,
                "pmcid": paper.pmcid,
                "doi": paper.doi,
                "title": paper.title
            }
        )


    # ========================================================
    # Docking Result
    # ========================================================

    def add_docking_result(
        self,
        result: DockingResultEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_DOCKING_RESULT,
            result.model_dump()
        )


    # ========================================================
    # Clear Entire Graph
    # ========================================================

    def clear_graph(self):

        self.client.execute_query(
            graph_queries.CLEAR_GRAPH
        )


    # |=================================|
    # | ADD RELATIONSHIPS BETWEEN NODES |
    # |=================================|


    # ========================================================
    # Paper -> Compound
    # MENTIONS
    # ========================================================

    def add_paper_mentions_compound(
        self,
        paper: PaperEntity,
        compound: CompoundEntity
    ):

        paper_id = (
            paper.pmid
            or paper.pmcid
            or paper.doi
        )

        if not paper_id:
            raise ValueError(
                "Paper must have PMID, PMCID, or DOI."
            )

        self.client.execute_query(
            graph_queries.ADD_PAPER_MENTIONS_COMPOUND,
            {
                "paper_id": paper_id,
                "chembl_id": compound.chembl_id
            }
        )


    # ========================================================
    # Compound -> Protein
    # INTERACTION
    # ========================================================

    def add_compound_protein_interaction(
        self,
        compound: CompoundEntity,
        protein: ProteinEntity,
        interaction,
    ):

        self.client.execute_query(
            graph_queries.ADD_COMPOUND_PROTEIN_INTERACTION,
            {
                "chembl_id": compound.chembl_id,
                "uniprot_id": protein.uniprot_id,
                "interaction": interaction
            }
        )


    # ========================================================
    # Compound -> Disease
    # TREATS
    # ========================================================

    def add_compound_treats_disease(
        self,
        compound: CompoundEntity,
        disease: DiseaseEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_COMPOUND_TREATS_DISEASE,
            {
                "chembl_id": compound.chembl_id,
                "disease_id": disease.disease_id
            }
        )


    # ========================================================
    # Compound -> Side Effect
    # CAN_CAUSE
    # ========================================================

    def add_compound_can_cause_side_effect(
        self,
        compound: CompoundEntity,
        side_effect: SideEffectEntity
    ):

        self.client.execute_query(
            graph_queries.ADD_COMPOUND_CAN_CAUSE_SIDE_EFFECT,
            {
                "chembl_id": compound.chembl_id,
                "meddra_id": side_effect.meddra_id
            }
        )


    # ========================================================
    # Compound -> Compound
    # SIMILAR_TO
    # ========================================================

    def add_compound_similarity(
        self,
        query_compound: CompoundEntity,
        target_compound: CompoundEntity,
        similarity_score: float
    ):
        
        self.client.execute_query(
            graph_queries.ADD_COMPOUND_SIMILAR_TO_COMPOUND,
            {
                "query_chembl_id": query_compound.chembl_id,
                "target_chembl_id": target_compound.chembl_id,
                "similarity_score": similarity_score
            }
        )


    # |=================================|
    # | DELETE THE GRAPH NODES          |
    # |=================================|


    # ========================================================
    # Compound
    # ========================================================

    def delete_compound(
        self,
        chembl_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_COMPOUND,
            {
                "chembl_id": chembl_id
            }
        )


    # ========================================================
    # Protein
    # ========================================================

    def delete_protein(
        self,
        uniprot_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_PROTEIN,
            {
                "uniprot_id": uniprot_id
            }
        )


    # ========================================================
    # Disease
    # ========================================================

    def delete_disease(
        self,
        disease_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_DISEASE,
            {
                "disease_id": disease_id
            }
        )


    # ========================================================
    # Side Effect
    # ========================================================

    def delete_side_effect(
        self,
        meddra_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_SIDE_EFFECT,
            {
                "meddra_id": meddra_id
            }
        )


    # ========================================================
    # Pathway
    # ========================================================

    def delete_pathway(
        self,
        kegg_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_PATHWAY,
            {
                "kegg_id": kegg_id
            }
        )


    # ========================================================
    # Paper
    # ========================================================

    def delete_paper(
        self,
        paper_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_PAPER,
            {
                "paper_id": paper_id
            }
        )


    # ========================================================
    # Docking Result
    # ========================================================

    def delete_docking_result(
        self,
        docking_id: str
    ):

        self.client.execute_query(
            graph_queries.DELETE_DOCKING_RESULT,
            {
                "docking_id": docking_id
            }
        )



graph_service = GraphService(
    uri=settings.NEO4J_URI,
    username=settings.NEO4J_USERNAME,
    password=settings.NEO4J_PASSWORD
)