import { useContext } from "react";
import {
  ChevronLeft,
  ChevronRight,
  CircleCheck,
  ShieldCheck,
  TriangleAlert,
  CirclePile
} from "lucide-react";

import { StoreContext } from "../../context/StoredContext";

import "./Compound.css";

const Compound = ({
  compound_details,
  onPrevious,
  onNext,
  hasPrevious,
  hasNext,
  currentIndex,
  totalCompounds,
}) => {
  const compound = compound_details.compound;
  const properties = compound_details.properties;
  const synonyms = compound.synonyms ?? [];

  const { url } = useContext(StoreContext);
  const imageUrl = `${url}image/${encodeURIComponent(compound.chembl_id)}.svg`;

  return (
    <main className="compound">
      <header className="title-container">
        <div className="icon"><CirclePile size={16}/></div>
        <div className="title">
          <h2>{compound.canonical_name}</h2>
          <h3>
            <div className="synonyms">
              {synonyms.map((s, index) => {
                return (
                  <span key={s.syn_type}>
                    <p style={{ width: "fit-content" }}>{s.syn_type}: </p>
                    <p>{s.molecule_synonym}</p>
                    {index !== synonyms.length - 1 && (
                      <span className="dot">.</span>
                    )}
                  </span>
                );
              })}
            </div>

            <div className="compound-navigation">
              <button
                type="button"
                onClick={onPrevious}
                disabled={!hasPrevious}
                aria-label="Previous compound"
                title="Previous compound"
              >
                <ChevronLeft size={16} />
                <p>Previous</p>
              </button>
              <span>
                {currentIndex + 1} / {totalCompounds}
              </span>
              <button type="button" onClick={onNext} disabled={!hasNext}>
                <p>Next</p>
                <ChevronRight size={16} />
              </button>
            </div>

            <div className="indexed">
              <CircleCheck size={17} />
              <p>INDEXED</p>
            </div>
          </h3>
        </div>
      </header>

      <section className="compound-container">
        <div className="compound-item">
          <div className="compound-details">
            <div className="item">
              <div className="title-container">
                <div className="title">
                  <h2>Compound Information</h2>
                </div>
              </div>

              <div className="details">
                <div className="items">
                  <h3>SMILES</h3>
                  <span>{compound.smiles}</span>
                </div>
                <div className="items">
                  <h3>INCHIKEY</h3>
                  <span>{compound.inchikey}</span>
                </div>
                <div className="items cluster">
                  <div className="cluster-item">
                    <h3>MOLECULAR FORMULA</h3>
                    <span>{compound.molecular_formula}</span>
                  </div>
                  <div className="cluster-item">
                    <h3>CHEMBL ID</h3>
                    <span>{compound.chembl_id}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="image">
              <img
                src={imageUrl}
                alt={`${compound.canonical_name} structure`}
                onError={(event) => {
                  event.currentTarget.alt = "Compound structure unavailable";
                }}
              />
            </div>
          </div>

          <div className="lipinski">
            <div className="title">
              <h2>Lipinski's Rule of 5</h2>
              <ShieldCheck size={18} />
            </div>

            <div className="details">
              <div className="items">
                <h4>MW &le; 500 Da</h4>
                <div className="value">
                  <h4>{properties.molecular_weight.toFixed(2)}</h4>
                  {properties.lipinski.molecular_weight_pass ? (
                    <p className="pass">PASS</p>
                  ) : (
                    <p className="fail">FAIL</p>
                  )}
                </div>
              </div>
              <div className="items">
                <h4>LogP &le; 5</h4>
                <div className="value">
                  <h4>{properties.logp.toFixed(2)}</h4>
                  {properties.lipinski.logp_pass ? (
                    <p className="pass">PASS</p>
                  ) : (
                    <p className="fail">FAIL</p>
                  )}
                </div>
              </div>
              <div className="items">
                <h4>H-Bond Donors &le; 5</h4>
                <div className="value">
                  <h4>{properties.h_bond_donors}</h4>
                  {properties.lipinski.hbd_pass ? (
                    <p className="pass">PASS</p>
                  ) : (
                    <p className="fail">FAIL</p>
                  )}
                </div>
              </div>
              <div className="items">
                <h4>H-Bond Acceptors &le; 10</h4>
                <div className="value">
                  <h4>{properties.h_bond_acceptors}</h4>
                  {properties.lipinski.hba_pass ? (
                    <p className="pass">PASS</p>
                  ) : (
                    <p className="fail">FAIL</p>
                  )}
                </div>
              </div>
            </div>

            <div className="overall">
              {properties.lipinski.overall_pass ? (
                <>
                  <CircleCheck color="#0649db" size={18} />
                  <div className="title">
                    <h4>PASS - Lipinski Compliant</h4>
                    <span>
                      Compound exhibits optimal physicochemical properties for
                      oral bioavailability.
                    </span>
                  </div>
                </>
              ) : (
                <>
                  <TriangleAlert color="orangered" size={18} />
                  <div className="title">
                    <h4>
                      {properties.lipinski.violations} - Lipinski violations
                    </h4>
                    <span>
                      Compound exhibits unoptimal physicochemical properties for
                      oral bioavailability.
                    </span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="properties">
          <div className="title">
            <h3>PHYSICOCHEMICAL METRICS</h3>
          </div>

          <div className="details">
            <div className="items">
              <h3>MOLECUALR WEIGHT</h3>
              <h4>{properties.molecular_weight.toFixed(2)}</h4>
            </div>
            <div className="items">
              <h3>LOGP</h3>
              <h4>{properties.logp.toFixed(2)}</h4>
            </div>
            <div className="items">
              <h3>TPSA</h3>
              <h4>{properties.tpsa.toFixed(2)}</h4>
            </div>
            <div className="items">
              <h3>H-BOND DONORS</h3>
              <h4>{properties.h_bond_donors}</h4>
            </div>
            <div className="items">
              <h3>H-BOND ACCEPTORS</h3>
              <h4>{properties.h_bond_acceptors}</h4>
            </div>
            <div className="items">
              <h3>ROTATABLE BONDS</h3>
              <h4>{properties.rotatable_bonds}</h4>
            </div>
            <div className="items">
              <h3>HEAVY ATOM COUNT</h3>
              <h4>{properties.heavy_atom_count}</h4>
            </div>
            <div className="items">
              <h3>RING COUNT</h3>
              <h4>{properties.ring_count}</h4>
            </div>
            <div className="items">
              <h3>AROMATIC RING COUNT</h3>
              <h4>{properties.aromatic_ring_count}</h4>
            </div>
            <div className="items">
              <h3>FORMAL CHARGE</h3>
              <h4>{properties.formal_charge}</h4>
            </div>
            <div className="items">
              <h3>FRACTION CSP3</h3>
              <h4>{properties.fraction_csp3.toFixed(2)}</h4>
            </div>
            <div className="items">
              <h3>QED</h3>
              <h4>{properties.qed.toFixed(2)}</h4>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
};

export default Compound;
