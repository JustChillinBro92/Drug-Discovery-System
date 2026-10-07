import { useContext } from "react";

import { Download, Plus, Search, SquareArrowOutUpRight } from "lucide-react";

import { StoreContext } from "../../../context/StoredContext";

import "./RecentCompunds.css";

import data from "../../../assets/data";

const RecentCompunds = () => {
  return (
    <main className="recent-compounds">
      <section className="recent-compounds-card">
        <div className="recent-compounds-heading">
          <div>
            <div className="recent-compounds-route">
              <span>COMPOUND DISCOVERY</span>
              <span>/</span>
              <strong>RECENT COMPOUNDS</strong>
            </div>
            <h1>Recent Compounds Registry</h1>
            <p>
              Session catalog of analyzed small molecules, molecular properties,
              and Lipinski Ro5 compliance.
            </p>
          </div>

          <div className="recent-compounds-actions">
            <button type="button" className="export-button">
              <Download size={16} />
              Export CSV
            </button>
            <button type="button" className="screen-button">
              <Plus size={18} />
              Screen New Molecule
            </button>
          </div>
        </div>

        <div className="recent-compounds-toolbar">
          <label className="recent-compounds-search">
            <Search size={18} />
            <input
              type="search"
              placeholder="Filter compounds by name, ChEMBL ID, formula..."
            />
          </label>

          <label className="recent-compounds-sort">
            <span>SORT :</span>
            <select defaultValue="recent">
              <option value="recent">Recently Added</option>
              <option value="name">Name</option>
              <option value="chembl">ChEMBL ID</option>
              <option value="chembl">Molecular Weight</option>
              <option value="chembl">LogP</option>  
            </select>
          </label>
        </div>
      </section>

      <section className="recent-compounds-card">
        <div className="compounds-heading">
          <div className="compounds-title">
            <h4>All Registry Entries</h4>
            <span>3 of 120</span>
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
          <p>STRUCTURE</p>
          <p>COMPOUND NAME</p>
          <p>IDENTIFIERS</p>
          <p>MOL FORMULA</p>
          <p>MOL WGT</p>
          <p>LOGP</p>
          <p>LIPINSKI</p>
          <p>ACTIONS</p>
        </div>

        <div className="list">
          {data.state.analyzed_compounds.map((c) => {
            const compound = c.compound_details.compound;
            const properties = c.compound_details.properties;
            const synonyms = compound.synonyms ?? [];

            const { url } = useContext(StoreContext);
            const imageUrl = `${url}image/${encodeURIComponent(compound.chembl_id)}.svg`;

            return (
              <div className="list-item" key={compound.chembl_id}>
                <div className="img">
                  <img src={imageUrl} alt="" />
                </div>
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
                  <h5>{compound.chembl_id}</h5>
                </div>
                <div className="item">
                  <h3>{compound.molecular_formula}</h3>
                </div>
                <div className="item">
                  <h3>{properties.molecular_weight.toFixed(2)} Da</h3>
                </div>
                <div className="item">
                  <h3>{properties.logp.toFixed(2)}</h3>
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

export default RecentCompunds;
