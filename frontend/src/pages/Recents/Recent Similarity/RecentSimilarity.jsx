import { useState, useMemo } from "react";
import { Download, Plus, Search, CircleCheck, CirclePile } from "lucide-react";

import "./RecentSimilarity.css";

import { data } from "../../../assets/data";

const compounds = data.state.analyzed_compounds.map((c) => c.compound_details);

const RecentSimilarity = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("recent");

  const visibleCompounds = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();

    const filteredCompounds = compounds
      .map((c) => {
        if (!normalizedQuery) {
          return {
            c,
            searchScore: 0,
          };
        }

        const name = c.compound.canonical_name?.toLowerCase() || "";

        const text = [
          c.compound.canonical_name,
          c.compound.chembl_id,
          c.compound.molecular_formula,
          c.properties.molecular_weight,
          c.properties.logp,
          c.properties.lipinski.overall_pass ? "pass" : "fail",
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();

        if (name.startsWith(normalizedQuery)) {
          return {
            c,
            searchScore: 2,
          };
        }

        if (text.includes(normalizedQuery)) {
          return {
            c,
            searchScore: 1,
          };
        }

        return null;
      })
      .filter(Boolean);

    return filteredCompounds
      .sort((a, b) => {
        // Search relevance first
        if (normalizedQuery && a.searchScore !== b.searchScore) {
          return b.searchScore - a.searchScore;
        }

        // Then user's selected sorting
        if (sortBy === "name")
          return a.c.compound.canonical_name.localeCompare(
            b.c.compound.canonical_name,
          );
        if (sortBy === "compoundId")
          return a.c.compound.chembl_id.localeCompare(b.c.compound.chembl_id);
        if (sortBy === "weight")
          return (
            a.c.properties.molecular_weight - b.c.properties.molecular_weight
          );
        if (sortBy === "logp") return a.c.properties.logp - b.c.properties.logp;
      })
      .map(({ c }) => c);
  }, [compounds, searchQuery, sortBy]);

  const analyzed_compounds = data.state.analyzed_compounds;

  const getCompoundDetails = (chembl_id) => {
    const match = analyzed_compounds.find(
      (c) => c.compound_details.compound.chembl_id === chembl_id,
    );
    return match?.compound_details;
  };

  return (
    <main className="recent-compounds">
      <header className="recent-similarity-card">
        <div className="recent-compounds-heading">
          <div>
            <div className="recent-compounds-route">
              <span>COMPOUND DISCOVERY</span>
              <span>/</span>
              <strong>RECENT SIMILARITY</strong>
            </div>
            <h1>Recent Similarity Registry</h1>
            <p>
              Session catalog of analyzed similar compounds of query compounds
              and their similarity score
            </p>
          </div>

          <div className="recent-compounds-actions">
            <button type="button" className="export-button">
              <Download size={16} />
              Export CSV
            </button>
            <button type="button" className="screen-button">
              <Plus size={18} />
              Screen New Similarity
            </button>
          </div>
        </div>

        <div className="recent-compounds-toolbar">
          <label className="recent-compounds-search">
            <Search size={18} />
            <input
              type="search"
              placeholder="Filter query compounds by name, ChEMBL ID, formula..."
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </label>

          <label className="recent-compounds-sort">
            <span>SORT :</span>
            <select
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value)}
            >
              <option value="recent">Recently Added</option>
              <option value="name">Compound Name</option>
              <option value="compoundId">Compound ID</option>
              <option value="weight">Molecular Weight</option>
              <option value="logp">LogP Value</option>
            </select>
          </label>
        </div>
      </header>

      <section className="recent-similarity-compound">
        {Array.from(
          data.state.similarity_results.reduce((groups, result) => {
            const queryResults = groups.get(result.query_chembl_id) ?? [];
            queryResults.push(result);
            groups.set(result.query_chembl_id, queryResults);
            return groups;
          }, new Map()),
        ).map(([queryChemblId, results]) => {
          const compoundDetails = getCompoundDetails(queryChemblId);

          const compound = compoundDetails.compound;
          const synonyms = compound.synonyms ?? [];

          return (
            <div
              className="recent-similarity-card similarity-group"
              key={compound.chembl_id}
            >
              <header className="title-container">
                <div className="icon">
                  <CirclePile size={16} />
                </div>
                <div className="title">
                  <h2>
                    {compound.canonical_name}
                    <span>{compound.chembl_id}</span>
                    <span>{compound.molecular_formula}</span>
                  </h2>
                  <h3>
                    <div className="synonyms">
                      {synonyms.map((s, index) => {
                        return (
                          <span key={s.syn_type}>
                            <p style={{ width: "fit-content" }}>
                              {s.syn_type}:{" "}
                            </p>
                            <p>{s.molecule_synonym}</p>
                            {index !== synonyms.length - 1 && (
                              <span className="dot">.</span>
                            )}
                          </span>
                        );
                      })}
                    </div>

                    <div className="compounds-legend">
                      <span className="legend-item compliant">
                        <CircleCheck size={13} />
                        Lipinski Compliant
                      </span>
                    </div>
                  </h3>
                </div>
              </header>

              <div className="similarity-results-grid">
                {results.map((result) => {
                  const targetDetails = getCompoundDetails(result.chembl_id);

                  const targetCompound = targetDetails.compound;
                  const score = result.similarity_score.toFixed(2);

                  return (
                    <article
                      className="similar-compound-card"
                      key={`${queryChemblId}-${result.chembl_id}`}
                    >
                      <div className="similar-compound-card-heading">
                        <h2>{targetCompound.canonical_name}</h2>
                        <div className="score">
                          {score * 100}%
                          <div className="score-bar">
                            <div
                              className="bar-fill"
                              style={{ width: `${score * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>

                      <div className="similar-compound-card-details">
                        <div className="details">
                          <span>{targetCompound.chembl_id}</span>
                          <span>{targetCompound.molecular_formula}</span>
                        </div>

                        <div className="compounds-legend">
                          {score >= 0.7 ? (
                            <span className="moderate-legend-item compliant">
                              Very High Similarity
                            </span>
                          ) : score >= 0.5 ? (
                            <span className="legend-item compliant">
                              High Similarity
                            </span>
                          ) : score >= 0.3 ? (
                            <span className="moderate-legend-item moderate">
                              Moderate Similarity
                            </span>
                          ) : (
                            <span className="legend-item flagged">
                              Low Similarity
                            </span>
                          )}
                        </div>
                      </div>
                    </article>
                  );
                })}
              </div>
            </div>
          );
        })}
      </section>
    </main>
  );
};

export default RecentSimilarity;
