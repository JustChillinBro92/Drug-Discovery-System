export const data = {
  state: {
    analyzed_compounds: [
      {
        compound_details: {
          compound: {
            original_text: "aspirin",
            canonical_name: "ASPIRIN",
            confidence: 1,
            chembl_id: "CHEMBL25",
            smiles: "CC(=O)Oc1ccccc1C(=O)O",
            inchikey: "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
            molecular_formula: "C9H8O4",
            synonyms: [
              {
                molecule_synonym: "Acetylsalicylic acid",
                syn_type: "ATC",
                synonyms: "ACETYLSALICYLIC ACID",
              },
              {
                molecule_synonym: "Aspirin",
                syn_type: "FDA",
                synonyms: "ASPIRIN",
              },
            ],
          },
          properties: {
            molecular_weight: 180.15899999999996,
            logp: 1.3101,
            tpsa: 63.60000000000001,
            h_bond_donors: 1,
            h_bond_acceptors: 3,
            rotatable_bonds: 2,
            heavy_atom_count: 13,
            ring_count: 1,
            aromatic_ring_count: 1,
            formal_charge: 0,
            fraction_csp3: 0.1111111111111111,
            qed: 0.5501217966938848,
            lipinski: {
              molecular_weight_pass: true,
              logp_pass: true,
              hbd_pass: true,
              hba_pass: true,
              overall_pass: true,
              violations: 0,
            },
          },
        },
        summary: {
          protein_count: 2,
          side_effect_count: 70,
          treatable_disease_count: 7,
        },
      },
      {
        compound_details: {
          compound: {
            original_text: "ibuprofen",
            canonical_name: "IBUPROFEN",
            confidence: 1,
            chembl_id: "CHEMBL521",
            smiles: "CC(C)Cc1ccc(C(C)C(=O)O)cc1",
            inchikey: "HEFNNWSXXWATRW-UHFFFAOYSA-N",
            molecular_formula: "C13H18O2",
            synonyms: [
              {
                molecule_synonym: "Ibuprofen",
                syn_type: "ATC",
                synonyms: "IBUPROFEN",
              },
              {
                molecule_synonym: "Ibuprofen",
                syn_type: "FDA",
                synonyms: "IBUPROFEN",
              },
            ],
          },
          properties: {
            molecular_weight: 206.28499999999997,
            logp: 3.073200000000001,
            tpsa: 37.3,
            h_bond_donors: 1,
            h_bond_acceptors: 1,
            rotatable_bonds: 4,
            heavy_atom_count: 15,
            ring_count: 1,
            aromatic_ring_count: 1,
            formal_charge: 0,
            fraction_csp3: 0.46153846153846156,
            qed: 0.8215995486924975,
            lipinski: {
              molecular_weight_pass: true,
              logp_pass: true,
              hbd_pass: true,
              hba_pass: true,
              overall_pass: true,
              violations: 0,
            },
          },
        },
        summary: {
          protein_count: 3,
          side_effect_count: 287,
          treatable_disease_count: 12,
        },
      },
      {
        compound_details: {
          compound: {
            original_text: "montelukast",
            canonical_name: "MONTELUKAST",
            confidence: 1,
            chembl_id: "CHEMBL787",
            smiles:
              "CC(C)(O)c1ccccc1CC[C@@H](SCC1(CC(=O)O)CC1)c1cccc(/C=C/c2ccc3ccc(Cl)cc3n2)c1",
            inchikey: "UCHDWCPVSPXUMX-TZIWLTJVSA-N",
            molecular_formula: "C35H36ClNO3S",
            synonyms: [
              {
                molecule_synonym: "Montelukast",
                syn_type: "ATC",
                synonyms: "MONTELUKAST",
              },
            ],
          },
          properties: {
            molecular_weight: 586.1970000000001,
            logp: 8.948000000000002,
            tpsa: 70.42,
            h_bond_donors: 2,
            h_bond_acceptors: 4,
            rotatable_bonds: 12,
            heavy_atom_count: 41,
            ring_count: 5,
            aromatic_ring_count: 4,
            formal_charge: 0,
            fraction_csp3: 0.3142857142857143,
            qed: 0.1735643864602374,
            lipinski: {
              molecular_weight_pass: false,
              logp_pass: false,
              hbd_pass: true,
              hba_pass: true,
              overall_pass: false,
              violations: 2,
            },
          },
        },
        summary: {
          protein_count: 18,
          side_effect_count: 121,
          treatable_disease_count: 2,
        },
      },
    ],
    similarity_results: [
      {
        query_original_text: "aspirin",
        query_compound: "ASPIRIN",
        compound_original_text: "ibuprofen",
        compound_name: "IBUPROFEN",
        chembl_id: "CHEMBL521",
        similarity_score: 0.1951219512195122,
      },
      {
        query_original_text: "aspirin",
        query_compound: "ASPIRIN",
        compound_original_text: "montelukast",
        compound_name: "MONTELUKAST",
        chembl_id: "CHEMBL787",
        similarity_score: 0.11627906976744186,
      },
    ],
    referenced_paper_ids: [
      "42536556",
      "42744697",
      "42686479",
      "42694880",
      "42509693",
      "42736584",
    ],
    literature_retrievals: {
      "31776aa0-0376-462e-b969-d8aae9a251bc": {
        query: "recent trends in cancer research",
        category: null,
        retrieved_chunk_ids: [
          "42744697_2",
          "42736584_3",
          "42694880_3",
          "42736584_2",
          "42736584_0",
          "42536556_2",
          "42509693_2",
          "42686479_1",
        ],
        referenced_papers: [
          {
            pmid: "42744697",
            pmcid: null,
            doi: "10.1016/j.molmed.2026.08.002",
            title:
              "hPSC models in cancer mechanisms and therapeutic discovery.",
            authors: ["Chu CW", "Chang YT", "Tat C", "Shoemaker R", "Lee DF"],
            keywords: [
              "Cancer Immunotherapy",
              "Tumor Microenvironment",
              "Personalized Oncology",
              "Organoids And Assembloids",
              "Ipsc-derived Cancer Models",
            ],
            journal: "Trends in molecular medicine",
            publication_year: 2026,
            url: "https://europepmc.org/article/MED/42744697",
          },
          {
            pmid: "42736584",
            pmcid: "PMC13573397",
            doi: "10.1186/s41512-026-00236-9",
            title:
              "The use of blood test trends in cancer detection: a scoping review.",
            authors: [
              "Zhu S",
              "Friedemann Smith C",
              "Collins KK",
              "Ziyenge SE",
              "Murphy J",
              "de Vere Hunt I",
              "Brubert Z",
              "Roberts N",
              "Morris EJA",
              "Hobbs R",
              "Nicholson BD",
              "Virdee PS",
            ],
            keywords: [
              "Repeated measurement",
              "Cancer Detection",
              "Scoping Review",
              "Blood Test Trend",
            ],
            journal: "Diagnostic and prognostic research",
            publication_year: 2026,
            url: "https://europepmc.org/article/MED/42736584",
          },
          {
            pmid: "42694880",
            pmcid: "PMC13539906",
            doi: "10.7150/ijms.137251",
            title:
              "Mapping the Evolutionary Landscape of Solid Tumor Immunotherapy: A Quarter-Century Bibliometric Analysis of the Title-Defined Core Literature (2000-2025).",
            authors: [
              "Ozcelik EE",
              "Akin G",
              "Odabasi Bukun H",
              "Sali M",
              "Sahin AB",
              "Deligonul A",
              "Cubukcu E",
              "Evrensel T",
            ],
            keywords: [
              "Cancer Immunotherapy",
              "Neoadjuvant Therapy",
              "Tumor Microenvironment",
              "Solid Tumors",
              "Bibliometric Analysis",
              "Checkpoint Inhibitors",
            ],
            journal: "International journal of medical sciences",
            publication_year: 2026,
            url: "https://europepmc.org/article/MED/42694880",
          },
          {
            pmid: "42536556",
            pmcid: "PMC13433093",
            doi: "10.1097/md.0000000000049910",
            title:
              "Mapping the evolution and impact of microfluidic technology research on cancer diagnosis: A comprehensive bibliometric analysis from 2015 to 2024.",
            authors: ["Su X", "Pu J", "Liao J", "Li J", "Huang J", "Wu Z"],
            keywords: [
              "bibliometrics",
              "Cancer Diagnosis",
              "Visual Analysis",
              "Microfluidic Technology",
            ],
            journal: "Medicine",
            publication_year: 2026,
            url: "https://europepmc.org/article/MED/42536556",
          },
          {
            pmid: "42509693",
            pmcid: null,
            doi: "10.2174/0115748928444498260516065557",
            title:
              "Innovative Therapeutic Strategies for Hormone-sensitive Breast Cancer: A Patent Landscape Review.",
            authors: [
              "Oliveira CE",
              "J\u00fanior JACN",
              "Santos CR",
              "Barreto PDC",
              "Alves IA",
            ],
            keywords: [
              "Patents",
              "Targeted Therapy",
              "Endocrine Resistance",
              "Hormone-sensitive Breast Cancer",
              "New Anticancer Drugs",
              "Innovative Treatments.",
            ],
            journal: "Recent patents on anti-cancer drug discovery",
            publication_year: 2026,
            url: "https://europepmc.org/article/MED/42509693",
          },
          {
            pmid: "42686479",
            pmcid: null,
            doi: "10.1016/j.trecan.2026.08.004",
            title: "Host metabolism rewrites metastatic fate.",
            authors: ["Qiu Z", "Li X", "Xu P"],
            keywords: [
              "Metastasis",
              "Colorectal Cancer",
              "hepatic steatosis",
              "Host Metabolism",
            ],
            journal: "Trends in cancer",
            publication_year: 2026,
            url: "https://europepmc.org/article/MED/42686479",
          },
        ],
        offset: 8,
      },
    },
    important_context: [],
  },
};

const compound_data = {
  compound: {
    original_text: "aspirin",
    canonical_name: "ASPIRIN",
    confidence: 1,
    chembl_id: "CHEMBL25",
    smiles: "CC(=O)Oc1ccccc1C(=O)O",
    inchikey: "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
    molecular_formula: "C9H8O4",
  },
  properties: {
    molecular_weight: 180.15899999999996,
    logp: 1.3101,
    tpsa: 63.60000000000001,
    h_bond_donors: 1,
    h_bond_acceptors: 3,
    rotatable_bonds: 2,
    heavy_atom_count: 13,
    ring_count: 1,
    aromatic_ring_count: 1,
    formal_charge: 0,
    fraction_csp3: 0.1111111111111111,
    qed: 0.5501217966938848,
  },
  drug_likeness: {
    lipinski: {
      molecular_weight: {
        value: 180.15899999999996,
        limit: "<= 500 Da",
        pass: true,
        explanation:
          "Molecular weight affects absorption and membrane permeability.",
      },
      logp: {
        value: 1.3101,
        limit: "<= 5",
        pass: true,
        explanation:
          "LogP represents lipophilicity and affects solubility and permeability.",
      },
      hydrogen_bond_donors: {
        value: 1,
        limit: "<= 5",
        pass: true,
        explanation:
          "Hydrogen bond donors influence protein interactions and permeability.",
      },
      hydrogen_bond_acceptors: {
        value: 3,
        limit: "<= 10",
        pass: true,
        explanation:
          "Hydrogen bond acceptors affect molecular interactions and solubility.",
      },
      overall: {
        pass: true,
        violations: 0,
        classification: "Drug-like",
        explanation:
          "Compound exhibits optimal physiochemical properties for oral bioavailibilty.",
      },
    },
  },
  proteins: [
    {
      target_chembl_id: "CHEMBL3253",
      target_name: "Albumin",
      organism: "Homo sapiens",
      accession: "P02768",
      component_description: "Albumin",
      component_type: "PROTEIN",
      interaction_type: "BINDS_TO",
      activities_no: 1,
      protein: {
        uniprot_id: "P02768",
        protein_name: "Albumin",
        gene_symbol: "ALB",
        organism: "Homo sapiens",
        function:
          "Binds water, Ca(2+), Na(+), K(+), fatty acids, hormones, bilirubin and drugs (Probable). Its main function is the regulation of the colloidal osmotic pressure of blood (Probable). Major zinc transporter in plasma, typically binds about 80% of all plasma zinc (PubMed:19021548). Major calcium and magnesium transporter in plasma, binds approximately 45% of circulating calcium and magnesium in plasma (By similarity). Potentially has more than two calcium-binding sites and might additionally bind calcium in a non-specific manner (By similarity). The shared binding site between zinc and calcium at residue Asp-273 suggests a crosstalk between zinc and calcium transport in the blood (By similarity). The rank order of affinity is zinc > calcium > magnesium (By similarity). Binds to the bacterial siderophore enterobactin and inhibits enterobactin-mediated iron uptake of E.coli from ferric transferrin, and may thereby limit the utilization of iron and growth of enteric bacteria such as E.coli (PubMed:6234017). Does not prevent iron uptake by the bacterial siderophore aerobactin (PubMed:6234017)",
        subcellular_location: "Secreted",
        pathways: [],
        sequence:
          "MKWVTFISLLFLFSSAYSRGVFRRDAHKSEVAHRFKDLGEENFKALVLIAFAQYLQQCPFEDHVKLVNEVTEFAKTCVADESAENCDKSLHTLFGDKLCTVATLRETYGEMADCCAKQEPERNECFLQHKDDNPNLPRLVRPEVDVMCTAFHDNEETFLKKYLYEIARRHPYFYAPELLFFAKRYKAAFTECCQAADKAACLLPKLDELRDEGKASSAKQRLKCASLQKFGERAFKAWAVARLSQRFPKAEFAEVSKLVTDLTKVHTECCHGDLLECADDRADLAKYICENQDSISSKLKECCEKPLLEKSHCIAEVENDEMPADLPSLAADFVESKDVCKNYAEAKDVFLGMFLYEYARRHPDYSVVLLLRLAKTYETTLEKCCAAADPHECYAKVFDEFKPLVEEPQNLIKQNCELFEQLGEYKFQNALLVRYTKKVPQVSTPTLVEVSRNLGKVGSKCCKHPEAKRMPCAEDYLSVVLNQLCVLHEKTPVSDRVTKCCTESLVNRRPCFSALEVDETYVPKEFNAETFTFHADICTLSEKERQIKKQTALVELVKHKPKATKEQLKAVMDDFAAFVEKCCKADDKETCFAEEGKKLVAASQAALGL",
        sequence_length: 609,
      },
    },
    {
      target_chembl_id: "CHEMBL230",
      target_name: "Prostaglandin G/H synthase 2",
      organism: "Homo sapiens",
      accession: "P35354",
      component_description: "Prostaglandin G/H synthase 2",
      component_type: "PROTEIN",
      interaction_type: "INHIBITS",
      activities_no: 2,
      protein: {
        uniprot_id: "P35354",
        protein_name: "Prostaglandin G/H synthase 2",
        gene_symbol: "PTGS2",
        organism: "Homo sapiens",
        function:
          "Dual cyclooxygenase and peroxidase in the biosynthesis pathway of prostanoids, a class of C20 oxylipins mainly derived from arachidonate ((5Z,8Z,11Z,14Z)-eicosatetraenoate, AA, C20:4(n-6)), with a particular role in the inflammatory response (PubMed:11939906, PubMed:16373578, PubMed:17519235, PubMed:19540099, PubMed:22942274, PubMed:26859324, PubMed:27226593, PubMed:7592599, PubMed:7947975, PubMed:9261177). The cyclooxygenase activity oxygenates AA to the hydroperoxy endoperoxide prostaglandin G2 (PGG2), and the peroxidase activity reduces PGG2 to the hydroxy endoperoxide prostaglandin H2 (PGH2), the precursor of all 2-series prostaglandins and thromboxanes (PubMed:16373578, PubMed:22942274, PubMed:26859324, PubMed:27226593, PubMed:7592599, PubMed:7947975, PubMed:9261177). This complex transformation is initiated by abstraction of hydrogen at carbon 13 (with S-stereochemistry), followed by insertion of molecular O2 to form the endoperoxide bridge between carbon 9 and 11 that defines prostaglandins. The insertion of a second molecule of O2 (bis-oxygenase activity) yields a hydroperoxy group in PGG2 that is then reduced to PGH2 by two electrons (PubMed:16373578, PubMed:22942274, PubMed:26859324, PubMed:27226593, PubMed:7592599, PubMed:7947975, PubMed:9261177). Similarly catalyzes successive cyclooxygenation and peroxidation of dihomo-gamma-linoleate (DGLA, C20:3(n-6)) and eicosapentaenoate (EPA, C20:5(n-3)) to PGH1 and PGH3, the precursors of 1- and 3-series prostaglandins respectively, though arachidonate (AA, C20:4(n-6)) remains the preferred substrate (PubMed:11939906, PubMed:17519235, PubMed:19540099). In an alternative pathway of prostanoid biosynthesis, converts 2-arachidonoyl lysophospholipids to prostanoid lysophospholipids, which are then hydrolyzed by intracellular phospholipases to release free prostanoids (PubMed:27642067). Metabolizes 2-arachidonoyl glycerol yielding the glyceryl ester of PGH2, a process that can contribute to pain response (PubMed:22942274). Generates lipid mediators from n-3 and n-6 polyunsaturated fatty acids (PUFAs) via a lipoxygenase-type mechanism. Oxygenates PUFAs to hydroperoxy compounds and then reduces them to corresponding alcohols (PubMed:11034610, PubMed:11192938, PubMed:9048568, PubMed:9261177). Plays a role in the generation of resolution phase interaction products (resolvins) during both sterile and infectious inflammation (PubMed:12391014). Metabolizes docosahexaenoate (DHA, C22:6(n-3)) to 17R-HDHA, a precursor of the D-series resolvins (RvDs) (PubMed:12391014). As a component of the biosynthetic pathway of E-series resolvins (RvEs), converts eicosapentaenoate (EPA, C20:5(n-3)) primarily to 18S-HEPE that is further metabolized by ALOX5 and LTA4H to generate 18S-RvE1 and 18S-RvE2 (PubMed:21206090). In vascular endothelial cells, converts docosapentaenoate (DPA, C22:5(n-3)) to 13R-HDPA, a precursor for 13-series resolvins (RvTs) shown to activate macrophage phagocytosis during bacterial infection (PubMed:26236990). In activated leukocytes, contributes to oxygenation of hydroxyeicosatetraenoates (HETE) to diHETES (5,15-diHETE and 5,11-diHETE) (PubMed:22068350, PubMed:26282205). Can also use linoleate (LA, (9Z,12Z)-octadecadienoate, C18:2(n-6)) as substrate and produce hydroxyoctadecadienoates (HODEs) in a regio- and stereospecific manner, being (9R)-HODE ((9R)-hydroxy-(10E,12Z)-octadecadienoate) and (13S)-HODE ((13S)-hydroxy-(9Z,11E)-octadecadienoate) its major products (By similarity) (PubMed:7642610). During neuroinflammation, plays a role in neuronal secretion of specialized preresolving mediators (SPMs) 15R-lipoxin A4 that regulates phagocytic microglia (By similarity)",
        subcellular_location:
          "Microsome membrane, Endoplasmic reticulum membrane, Nucleus inner membrane, Nucleus outer membrane",
        pathways: ["Lipid metabolism; prostaglandin biosynthesis"],
        sequence:
          "MLARALLLCAVLALSHTANPCCSHPCQNRGVCMSVGFDQYKCDCTRTGFYGENCSTPEFLTRIKLFLKPTPNTVHYILTHFKGFWNVVNNIPFLRNAIMSYVLTSRSHLIDSPPTYNADYGYKSWEAFSNLSYYTRALPPVPDDCPTPLGVKGKKQLPDSNEIVEKLLLRRKFIPDPQGSNMMFAFFAQHFTHQFFKTDHKRGPAFTNGLGHGVDLNHIYGETLARQRKLRLFKDGKMKYQIIDGEMYPPTVKDTQAEMIYPPQVPEHLRFAVGQEVFGLVPGLMMYATIWLREHNRVCDVLKQEHPEWGDEQLFQTSRLILIGETIKIVIEDYVQHLSGYHFKLKFDPELLFNKQFQYQNRIAAEFNTLYHWHPLLPDTFQIHDQKYNYQQFIYNNSILLEHGITQFVESFTRQIAGRVAGGRNVPPAVQKVSQASIDQSRQMKYQSFNEYRKRFMLKPYESFEELTGEKEMSAELEALYGDIDAVELYPALLVEKPRPDAIFGETMVEVGAPFSLKGLMGNVICSPAYWKPSTFGGEVGFQIINTASIQSLICNNVKGCPFTSFSVPDPELIKTVTINASSSRSGLDDINPTVLLKERSTEL",
        sequence_length: 604,
      },
    },
  ],
  side_effects: [
    {
      meddra_id: "C0002792",
      side_effect_name: "Anaphylactic shock",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0002871",
      side_effect_name: "Anaemia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0002994",
      side_effect_name: "Angioedema",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0004096",
      side_effect_name: "Asthma",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0008031",
      side_effect_name: "Chest pain",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0009421",
      side_effect_name: "Coma",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0009676",
      side_effect_name: "Confusional state",
      meddra_level: "PT",
    },
    {
      meddra_id: "C1443060",
      side_effect_name: "Feeling abnormal",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0011991",
      side_effect_name: "Diarrhoea",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0012833",
      side_effect_name: "Dizziness",
      meddra_level: "PT",
    },
    {
      meddra_id: "C2830004",
      side_effect_name: "Somnolence",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0013395",
      side_effect_name: "Dyspepsia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0013404",
      side_effect_name: "Dyspnoea",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0015230",
      side_effect_name: "Rash",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0011603",
      side_effect_name: "Dermatitis",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0016382",
      side_effect_name: "Flushing",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0019080",
      side_effect_name: "Haemorrhage",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0518015",
      side_effect_name: "Haemoglobin",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0020517",
      side_effect_name: "Hypersensitivity",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0020538",
      side_effect_name: "Hypertension",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0020621",
      side_effect_name: "Hypokalaemia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0023530",
      side_effect_name: "Leukopenia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0027497",
      side_effect_name: "Nausea",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0033774",
      side_effect_name: "Pruritus",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0036572",
      side_effect_name: "Convulsion",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0036974",
      side_effect_name: "Shock",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0020458",
      side_effect_name: "Hyperhidrosis",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0039231",
      side_effect_name: "Tachycardia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0040034",
      side_effect_name: "Thrombocytopenia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0042109",
      side_effect_name: "Urticaria",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0042963",
      side_effect_name: "Vomiting",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0085631",
      side_effect_name: "Agitation",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0151763",
      side_effect_name: "Hepatocellular injury",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0235710",
      side_effect_name: "Chest discomfort",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0002064",
      side_effect_name: "Respiratory alkalosis",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0005779",
      side_effect_name: "Coagulopathy",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0006147",
      side_effect_name: "Breast feeding",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0008049",
      side_effect_name: "Varicella",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0009938",
      side_effect_name: "Contusion",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0011849",
      side_effect_name: "Diabetes mellitus",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0032617",
      side_effect_name: "Polyuria",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0017181",
      side_effect_name: "Gastrointestinal haemorrhage",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0018099",
      side_effect_name: "Gout",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0018926",
      side_effect_name: "Haematemesis",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0019087",
      side_effect_name: "Haemorrhagic disorder",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0020615",
      side_effect_name: "Hypoglycaemia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0023895",
      side_effect_name: "Liver disorder",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0239571",
      side_effect_name: "Foetor hepaticus",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0025222",
      side_effect_name: "Melaena",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0030920",
      side_effect_name: "Peptic ulcer",
      meddra_level: "PT",
    },
    {
      meddra_id: "C1368065",
      side_effect_name: "Vascular purpura",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0034150",
      side_effect_name: "Purpura",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0035400",
      side_effect_name: "Reye's syndrome",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0041657",
      side_effect_name: "Loss of consciousness",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0039070",
      side_effect_name: "Syncope",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0039971",
      side_effect_name: "Thirst",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0040264",
      side_effect_name: "Tinnitus",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0041582",
      side_effect_name: "Ulcer",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0042571",
      side_effect_name: "Vertigo",
      meddra_level: "PT",
    },
    {
      meddra_id: "C1565489",
      side_effect_name: "Renal impairment",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0220981",
      side_effect_name: "Metabolic acidosis",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0235378",
      side_effect_name: "Hepatotoxicity",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0001122",
      side_effect_name: "Acidosis",
      meddra_level: "PT",
    },
    {
      meddra_id: "C1291078",
      side_effect_name: "Epigastric discomfort",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0003862",
      side_effect_name: "Arthralgia",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0021400",
      side_effect_name: "Influenza",
      meddra_level: "PT",
    },
    {
      meddra_id: "C1145670",
      side_effect_name: "Respiratory failure",
      meddra_level: "PT",
    },
    {
      meddra_id: "C1384666",
      side_effect_name: "Hearing impaired",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0011053",
      side_effect_name: "Deafness",
      meddra_level: "PT",
    },
    {
      meddra_id: "C0595930",
      side_effect_name: "Blood cholesterol increased",
      meddra_level: "PT",
    },
  ],
  diseases: [
    {
      mesh_id: "D005334",
      mesh_concept_id: "M0008421",
      disease_name: "Fever",
      description:
        "An abnormal elevation of body temperature, usually as a result of a pathologic process.",
    },
    {
      mesh_id: "D010146",
      mesh_concept_id: "M0015742",
      disease_name: "Pain",
      description:
        "An unpleasant sensation induced by noxious stimuli which are detected by NERVE ENDINGS of NOCICEPTIVE NEURONS.",
    },
    {
      mesh_id: "D001172",
      mesh_concept_id: "M0001750",
      disease_name: "Arthritis, Rheumatoid",
      description:
        "A chronic systemic disease, primarily of the joints, marked by inflammatory changes in the synovial membranes and articular structures, widespread fibrinoid degeneration of the collagen fibers in mesenchymal tissues, and by atrophy and rarefaction of bony structures. Etiology is unknown, but autoimmune mechanisms have been implicated.",
    },
    {
      mesh_id: "D006073",
      mesh_concept_id: "M0009557",
      disease_name: "Gout",
      description:
        "Metabolic disorder characterized by recurrent acute arthritis, hyperuricemia and deposition of sodium urate in and around the joints, sometimes with formation of URIC ACID calculi.",
    },
    {
      mesh_id: "D007249",
      mesh_concept_id: "M0011307",
      disease_name: "Inflammation",
      description:
        "A pathological process characterized by injury or destruction of tissues caused by a variety of cytologic and chemical reactions. It is usually manifested by typical signs of pain, heat, redness, swelling, and loss of function.",
    },
    {
      mesh_id: "D010003",
      mesh_concept_id: "M0015509",
      disease_name: "Osteoarthritis",
      description:
        "A progressive, degenerative joint disease, the most common form of arthritis, especially in older persons. The disease is thought to result not from the aging process but from biochemical changes and biomechanical stresses affecting articular cartilage. In the foreign literature it is often called osteoarthrosis deformans.",
    },
    {
      mesh_id: "D012213",
      mesh_concept_id: "M0019009",
      disease_name: "Rheumatic Fever",
      description:
        "A febrile disease occurring as a delayed sequela of infections with STREPTOCOCCUS PYOGENES. It is characterized by multiple focal inflammatory lesions of the connective tissue structures, such as the heart, blood vessels, and joints (POLYARTHRITIS) and brain, and by the presence of ASCHOFF BODIES in the myocardium and skin.",
    },
  ],
};

export const similarity_data = {
  compound: {
    original_text: "aspirin",
    canonical_name: "ASPIRIN",
    confidence: 1.0,
    chembl_id: "CHEMBL25",
    smiles: "CC(=O)Oc1ccccc1C(=O)O",
    inchikey: "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
    molecular_formula: "C9H8O4",
    synonyms: [
      {
        molecule_synonym: "Acetylsalicylic acid",
        value: "ACETYLSALICYLIC ACID",
        syn_type: "ATC",
      },
      {
        molecule_synonym: "Aspirin",
        value: "ASPIRIN",
        syn_type: "FDA",
      },
    ],
  },
  similarity_results: [
    {
      query_original_text: "aspirin",
      query_compound: "ASPIRIN",
      compound_original_text: "ibuprofen",
      compound_name: "IBUPROFEN",
      chembl_id: "CHEMBL521",
      similarity_score: 0.1951219512195122,
    },
    {
      query_original_text: "aspirin",
      query_compound: "ASPIRIN",
      compound_original_text: "montelukast",
      compound_name: "MONTELUKAST",
      chembl_id: "CHEMBL787",
      similarity_score: 0.11627906976744186,
    },
  ],
};

