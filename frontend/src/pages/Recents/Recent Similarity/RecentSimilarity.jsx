import { useState, useContext, useMemo } from "react";
import { Download, Plus, Search } from "lucide-react";

import { StoreContext } from "../../../context/StoredContext";

import "./RecentSimilarity.css"

import { data } from "../../../assets/data";

const compounds = data.state.analyzed_compounds.map((c) => 
  c.compound_details
);

const RecentSimilarity = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("recent");

  const { url } = useContext(StoreContext);

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

  return (
    <main className="recent-compounds">
      <section className="recent-similarity-card">
        <div className="recent-compounds-heading">
          <div>
            <div className="recent-compounds-route">
              <span>COMPOUND DISCOVERY</span>
              <span>/</span>
              <strong>RECENT SIMILARITY</strong>
            </div>
            <h1>Recent Similarity Registry</h1>
            <p>
              Session catalog of analyzed similar compounds of query compounds and their
              similarity score
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
      </section>


    </main>
  );
};

export default RecentSimilarity;
