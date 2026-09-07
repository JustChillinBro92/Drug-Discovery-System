# ========================================================
# GRAPH CONSTRAINTS
# ========================================================

CREATE_COMPOUND_CONSTRAINT = """
CREATE CONSTRAINT compound_chembl_id IF NOT EXISTS
FOR (c:Compound)
REQUIRE c.chembl_id IS UNIQUE
"""


CREATE_PROTEIN_CONSTRAINT = """
CREATE CONSTRAINT protein_uniprot_id IF NOT EXISTS
FOR (p:Protein)
REQUIRE p.uniprot_id IS UNIQUE
"""


CREATE_SIDE_EFFECT_CONSTRAINT = """
CREATE CONSTRAINT meddra_id IF NOT EXISTS
FOR (s:SideEffect)
REQUIRE s.meddra_id IS UNIQUE
"""


CREATE_DISEASE_CONSTRAINT = """
CREATE CONSTRAINT disease_id IF NOT EXISTS
FOR (d:Disease)
REQUIRE d.mesh_id IS UNIQUE
"""


CREATE_PAPER_CONSTRAINT = """
CREATE CONSTRAINT paper_id IF NOT EXISTS
FOR (p:Paper)
REQUIRE p.paper_id IS UNIQUE
"""


# ========================================================
# CREATE NODES
# ========================================================

ADD_COMPOUND = """
MERGE (c:Compound {
    chembl_id: $chembl_id
})

SET
    c.original_text = $original_text,
    c.canonical_name = $canonical_name,
    c.confidence = $confidence,
    c.smiles = $smiles,
    c.inchikey = $inchikey,
    c.molecular_formula = $molecular_formula,

    c.molecular_weight = $molecular_weight,
    c.logp = $logp,
    c.tpsa = $tpsa,
    c.h_bond_donors = $h_bond_donors,
    c.h_bond_acceptors = $h_bond_acceptors,
    c.rotatable_bonds = $rotatable_bonds,
    c.heavy_atom_count = $heavy_atom_count,
    c.ring_count = $ring_count,
    c.aromatic_ring_count = $aromatic_ring_count,
    c.formal_charge = $formal_charge,
    c.fraction_csp3 = $fraction_csp3,
    c.qed = $qed,

    c.lipinski_molecular_weight_pass = $lipinski_molecular_weight_pass,
    c.lipinski_logp_pass = $lipinski_logp_pass,
    c.lipinski_hbd_pass = $lipinski_hbd_pass,
    c.lipinski_hba_pass = $lipinski_hba_pass,
    c.lipinski_overall_pass = $lipinski_overall_pass,
    c.lipinski_violations = $lipinski_violations
"""


ADD_PROTEIN = """
MERGE (p:Protein {
    uniprot_id: $uniprot_id
})

SET
    p.protein_name = $protein_name,
    p.gene_symbol = $gene_symbol,
    p.organism = $organism,
    p.function = $function,
    p.subcellular_location = $subcellular_location,
    p.pathways = $pathways,
    p.sequence = $sequence,
    p.sequence_length = $sequence_length
"""


ADD_DISEASE = """
MERGE (d:Disease {
    mesh_id: $mesh_id
})

SET
    d.mesh_concept_id = $mesh_concept_id,
    d.disease_name = $disease_name,
    d.description = $description
"""


ADD_SIDE_EFFECT = """
MERGE (s:SideEffect {
    meddra_id: $meddra_id
})

SET
    s.side_effect_name = $side_effect_name,
    s.meddra_level = $meddra_level
"""


ADD_PATHWAY = """
MERGE (p:Pathway {
    kegg_id: $kegg_id
})

SET
    p.original_text = $original_text,
    p.canonical_name = $canonical_name,
    p.confidence = $confidence,
    p.synonyms = $synonyms,
    p.pathway_name = $pathway_name,
    p.organism = $organism
"""


ADD_PAPER = """
MERGE (p:Paper {
    paper_id: $paper_id
})

SET
    p.pmid = $pmid,
    p.pmcid = $pmcid,
    p.doi = $doi,
    p.title = $title
"""


ADD_DOCKING_RESULT = """
MERGE (d:DockingResult {
    docking_id: $docking_id
})

SET
    d.compound_id = $compound_id,
    d.protein_id = $protein_id,
    d.binding_affinity = $binding_affinity,
    d.docking_score = $docking_score,
    d.binding_mode = $binding_mode,
    d.software = $software
"""


# ========================================================
# RELATIONSHIPS
# ========================================================

ADD_PAPER_MENTIONS_COMPOUND = """
MATCH (p:Paper {
    paper_id: $paper_id
})

MATCH (c:Compound {
    chembl_id: $chembl_id
})

MERGE (p)-[:MENTIONS]->(c)
"""


ADD_COMPOUND_PROTEIN_INTERACTION = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

MATCH (p:Protein {
    uniprot_id: $uniprot_id
})

MERGE (c)-[r:$($interaction)]->(p)
SET
    r.interaction_type = $interaction,
    r.target_chembl_id = $target_chembl_id,
    r.target_name = $target_name,
    r.organism = $organism,
    r.component_description = $component_description,
    r.component_type = $component_type,
    r.activities_no = $activities_no
"""


ADD_COMPOUND_MAY_TREAT_DISEASE = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

MATCH (d:Disease {
    mesh_id: $mesh_id
})

MERGE (c)-[:MAY_TREAT]->(d)
"""


ADD_COMPOUND_CAN_CAUSE_SIDE_EFFECT = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

MATCH (s:SideEffect {
    meddra_id: $meddra_id
})

MERGE (c)-[:CAN_CAUSE]->(s)
"""


ADD_COMPOUND_SIMILAR_TO_COMPOUND = """
MATCH (c1:Compound {
    chembl_id: $query_chembl_id
})

MATCH (c2:Compound {
    chembl_id: $target_chembl_id
})

WHERE c1 <> c2

MERGE (c1)-[r:SIMILAR_TO]->(c2)

SET
    r.similarity_score = $similarity_score
"""


# ========================================================
# DELETE NODES
# ========================================================

DELETE_COMPOUND = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})
DETACH DELETE c
"""


DELETE_PROTEIN = """
MATCH (p:Protein {
    uniprot_id: $uniprot_id
})
DETACH DELETE p
"""


DELETE_DISEASE = """
MATCH (d:Disease {
    mesh_id: $mesh_id
})
DETACH DELETE d
"""


DELETE_SIDE_EFFECT = """
MATCH (s:SideEffect {
    meddra_id: $meddra_id
})
DETACH DELETE s
"""


DELETE_PATHWAY = """
MATCH (p:Pathway {
    kegg_id: $kegg_id
})
DETACH DELETE p
"""


DELETE_PAPER = """
MATCH (p:Paper {
    paper_id: $paper_id
})
DETACH DELETE p
"""


DELETE_DOCKING_RESULT = """
MATCH (d:DockingResult {
    docking_id: $docking_id
})
DETACH DELETE d
"""


# ========================================================
# CLEAR GRAPH
# ========================================================

CLEAR_GRAPH = """
MATCH (n)
DETACH DELETE n
"""


GET_COMPOUND_ANALYSIS = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

OPTIONAL MATCH (c)-[protein_relationship]->(p:Protein)
OPTIONAL MATCH (c)-[disease_relationship]->(d:Disease)
OPTIONAL MATCH (c)-[side_effect_relationship]->(s:SideEffect)

RETURN c,
    collect(DISTINCT {
        protein: p,
        target_chembl_id: protein_relationship[$target_chembl_property],
        target_name: protein_relationship[$target_name_property],
        organism: protein_relationship[$organism_property],
        component_description: protein_relationship[$description_property],
        component_type: protein_relationship[$component_type_property],
        activities_no: protein_relationship[$activities_property],
        interaction_type: coalesce(
            protein_relationship[$interaction_property],
            type(protein_relationship)
        )
    }) AS proteins,
    collect(DISTINCT CASE
        WHEN type(disease_relationship) = "MAY_TREAT" THEN d
    END) AS diseases,
    collect(DISTINCT CASE
        WHEN type(side_effect_relationship) = "CAN_CAUSE" THEN s
    END) AS side_effects
"""


GET_COMPOUND_ANALYSIS_BY_NAME = """
MATCH (c:Compound)
WHERE toLower(c[$canonical_property]) = toLower($compound_name)
    OR toLower(c[$original_property]) = toLower($compound_name)

OPTIONAL MATCH (c)-[protein_relationship]->(p:Protein)
OPTIONAL MATCH (c)-[disease_relationship]->(d:Disease)
OPTIONAL MATCH (c)-[side_effect_relationship]->(s:SideEffect)

RETURN c,
    collect(DISTINCT {
        protein: p,
        target_chembl_id: protein_relationship[$target_chembl_property],
        target_name: protein_relationship[$target_name_property],
        organism: protein_relationship[$organism_property],
        component_description: protein_relationship[$description_property],
        component_type: protein_relationship[$component_type_property],
        activities_no: protein_relationship[$activities_property],
        interaction_type: coalesce(
            protein_relationship[$interaction_property],
            type(protein_relationship)
        )
    }) AS proteins,
    collect(DISTINCT CASE
        WHEN type(disease_relationship) = "MAY_TREAT" THEN d
    END) AS diseases,
    collect(DISTINCT CASE
        WHEN type(side_effect_relationship) = "CAN_CAUSE" THEN s
    END) AS side_effects
LIMIT 1
"""