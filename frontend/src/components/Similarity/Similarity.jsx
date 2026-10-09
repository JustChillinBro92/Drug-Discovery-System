import { CircleCheck, SquareArrowOutUpRight, TextSearch } from "lucide-react";

import "./Similarity.css";

import { data, similarity_data } from "../../assets/data";

const Similarity = ({ reference_compound, similarity_results }) => {
  const compounds = data.state.analyzed_compounds;

  const getCompoundDetails = (chembl_id) => {
    const match = compounds.find(
      (c) => c.compound_details.compound.chembl_id === chembl_id,
    );
    return match?.compound_details;
  };

  return (
    <main className="similarity-results">
      <header className="title-container">
        <div className="icon">
          <TextSearch size={16} />
        </div>

        <div className="title">
          <h2>Simulated Pairwise Tanimoto Output</h2>
          <h3>
            <div className="synonyms">
              <span>
                <p>Pairwise calculations relative to query:</p>
                <p className="compound">
                  {similarity_data.compound.canonical_name}
                </p>
                <p className="compound">
                  ({similarity_data.compound.chembl_id})
                </p>
              </span>
            </div>
            <div className="indexed">
              <CircleCheck size={17} />
              <p>INDEXED</p>
            </div>
          </h3>
        </div>
      </header>

      <section className="recent-compounds-card">
        <div className="compounds-heading">
          <div className="compounds-title">
            <h4>All Registry Entries</h4>
            <span>{similarity_results.length}</span>
          </div>
          <div className="compounds-legend">
            <span className="legend-item compliant">
              <i className="legend-dot compliant-dot" />
              Lipinski Compliant
            </span>
            <span className="legend-item flagged">
              <i className="legend-dot flagged-dot" />
              Lipinski Flagged
            </span>
          </div>
        </div>

        <div className="grid-headings">
          <p>COMPOUND NAME</p>
          <p>TANIMOTO SCORE</p>
          <p>COMPOUND ID</p>
          <p>MOL FORMULA</p>
          <p>MOL WGT</p>
          <p>LIPINSKI</p>
          <p>ACTIONS</p>
        </div>

        <div className="list">
          {similarity_results.map((c) => {
            const compound_details = getCompoundDetails(c.chembl_id);

            const compound = compound_details.compound;
            const synonyms = compound.synonyms ?? [];
            const properties = compound_details.properties;

            return (
              <div className="list-item" key={compound.chembl_id}>
                <div className="item">
                  <h5>{compound.canonical_name}</h5>
                  {synonyms.map((s, index) => {
                    return (
                      <h3 key={s.syn_type}>
                        <p style={{ width: "fit-content" }}>{s.syn_type}: </p>
                        <p>{s.molecule_synonym}</p>
                        {index !== synonyms.length - 1 && (
                          <p className="dot">.</p>
                        )}
                      </h3>
                    );
                  })}
                </div>

                <div className="item">
                  <div className="score">
                    <h3>{c.similarity_score.toFixed(2)}</h3>
                    <div className="score-bar">
                        <div className="bar-fill"
                            style={{width: `${c.similarity_score * 100}%`}}
                        ></div>
                    </div>
                  </div>

                  

                  <div className="compounds-legend">
                    <span className="legend-item compliant">
                      High Similarity
                    </span>
                  </div>
                </div>

                <div className="item">
                  <h5>{compound.chembl_id}</h5>
                </div>

                <div className="item">
                  <h3>{compound.molecular_formula}</h3>
                </div>

                <div className="item">
                  <h3>{properties.molecular_weight.toFixed(2)} Da</h3>
                </div>

                <div className="item">
                  {properties.lipinski.overall_pass ? (
                    <span className="pass">
                      <i className="legend-dot compliant-dot" />
                      <p>Pass</p>
                    </span>
                  ) : (
                    <span className="fail">
                      <i className="legend-dot flagged-dot" />
                      <p>Fail</p>
                    </span>
                  )}
                </div>

                <div className="item">
                  <span className="view">
                    <h3>View</h3>
                    <SquareArrowOutUpRight size={11} />
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
};

export default Similarity;
