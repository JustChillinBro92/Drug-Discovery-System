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
    c.synonyms = $synonyms,
    c.smiles = $smiles,
    c.inchikey = $inchikey,
    c.molecular_formula = $molecular_formula
"""


ADD_PROTEIN = """
MERGE (p:Protein {
    uniprot_id: $uniprot_id
})

SET
    p.original_text = $original_text,
    p.canonical_name = $canonical_name,
    p.confidence = $confidence,
    p.synonyms = $synonyms,
    p.gene_symbol = $gene_symbol,
    p.protein_name = $protein_name,
    p.organism = $organism
"""


ADD_DISEASE = """
MERGE (d:Disease {
    disease_id: $disease_id
})

SET
    d.original_text = $original_text,
    d.canonical_name = $canonical_name,
    d.confidence = $confidence,
    d.synonyms = $synonyms,
    d.ontology = $ontology,
    d.mesh_id = $mesh_id
"""


ADD_SIDE_EFFECT = """
MERGE (s:SideEffect {
    sider_id: $sider_id
})

SET
    s.original_text = $original_text,
    s.canonical_name = $canonical_name,
    s.confidence = $confidence,
    s.synonyms = $synonyms,
    s.frequency = $frequency,
    s.severity = $severity
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


ADD_COMPOUND_BINDS_PROTEIN = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

MATCH (p:Protein {
    uniprot_id: $uniprot_id
})

MERGE (c)-[:BINDS_TO]->(p)
"""


ADD_COMPOUND_TREATS_DISEASE = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

MATCH (d:Disease {
    disease_id: $disease_id
})

MERGE (c)-[:TREATS]->(d)
"""


ADD_COMPOUND_CAUSES_SIDE_EFFECT = """
MATCH (c:Compound {
    chembl_id: $chembl_id
})

MATCH (s:SideEffect {
    sider_id: $sider_id
})

MERGE (c)-[:CAUSES]->(s)
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
    disease_id: $disease_id
})
DETACH DELETE d
"""


DELETE_SIDE_EFFECT = """
MATCH (s:SideEffect {
    sider_id: $sider_id
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