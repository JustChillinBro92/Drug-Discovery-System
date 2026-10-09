import { useState } from "react";
import {
  FlaskConical,
  Play,
  SquareMenu,
  Microscope,
  CirclePlus,
  X,
} from "lucide-react";

import Compound from "../../components/Compound/Compound";

import "./CompoundAnalysis.css";

import { data } from "../../assets/data";

const CompoundAnalysis = () => {
  const compounds = data.state.analyzed_compounds;
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <main className="compound-analysis">
      <section className="compound-card">
        <div className="compound-header">
          <div>
            <div className="route">
              <span>COMPOUND DISCOVERY</span>
              <span>/</span>
              <strong>COMPOUND ANALYSIS</strong>
            </div>
            <h1>Compound Ingestion &amp; Cheminformatics Analysis</h1>
            <p>Enter compound name (e.g., Aspirin, Ibuprofen, Paracetamol)</p>
          </div>
          <div className="engine-ready">
            <Microscope size={17} />
            <span>Engine Ready</span>
          </div>
        </div>

        <form className="analysis-form">
          <div className="compound-input">
            <FlaskConical size={18} />
            <input type="text" placeholder="Enter compound name" />
            <button type="button" className="clear-input">
              <X size={17} />
            </button>
          </div>
          <button type="submit" className="run-analysis">
            <Play size={17} />
            <span>Run Analysis</span>
          </button>
        </form>

        <div className="quick-samples">
          <span className="quick-samples-label">Quick Samples :</span>
          <button type="button" className="sample">
            Aspirin
          </button>
          <button type="button" className="sample">
            Ibuprofen
          </button>
          <button type="button" className="sample">
            Paracetamol
          </button>
          <button type="button" className="sample">
            Atorvastatin
          </button>
          <button type="button" className="sample">
            Doxorubicin
          </button>
        </div>

        <div className="analyzed-compounds">
          <div className="analyzed-compounds-heading">
            <span>
              <SquareMenu size={16} /> Compound Queue (To be analyzed) :
            </span>
            <span className="count">3 in workspace</span>
          </div>
          <div className="analyzed-compounds-list">
            <button type="button" className="queue-item">
              Aspirin
            </button>
            <button type="button" className="queue-item">
              Ibuprofen
            </button>
            <button type="button" className="queue-item">
              Paracetamol
            </button>
            <button type="button" className="queue-item add">
              <CirclePlus size={14} />
              ADD COMPOUND
            </button>
          </div>
        </div>
      </section>

      {compounds.length > 0 && (
        <Compound
          compound_details={compounds[activeIndex].compound_details}
          onPrevious={() => setActiveIndex((index) => Math.max(index - 1, 0))}
          onNext={() =>
            setActiveIndex((index) => Math.min(index + 1, compounds.length - 1))
          }
          hasPrevious={activeIndex > 0}
          hasNext={activeIndex < compounds.length - 1}
          currentIndex={activeIndex}
          totalCompounds={compounds.length}
        />
      )}
    </main>
  );
};

export default CompoundAnalysis;
