import {
  FlaskConical,
  Play,
  Microscope,
  CirclePlus,
  X,
  Target
} from "lucide-react";

import Similarity from "../../components/Similarity/Similarity";

import "./SimilarityAnalysis.css";

import { similarity_data } from "../../assets/data"

const SimilarityAnalysis = () => {
  return (
    <main className="compound-analysis">
      <section className="compound-card">
        <div className="compound-header">
          <div>
            <div className="route">
              <span>COMPOUND DISCOVERY</span>
              <span>/</span>
              <strong>SIMILARITY ANALYSIS</strong>
            </div>
            <h1>Compound Ingestion &amp; Similarity Analysis</h1>
            <p>Evaluate a reference query compound against custom target 
              compounds using Tanimoto Morgan fingerprint radius-2 scoring.
            </p>
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
          <button type="submit" className="run-similarity">
            <Play size={17} />
            <span>Run Similarity Analysis</span>
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

        <form className="analysis-form">
          <div className="compound-input">
            <FlaskConical size={18} />
            <input type="text" placeholder="Enter target compound name" />
            <button type="button" className="clear-input">
              <X size={17} />
            </button>
          </div>
          <button type="submit" className="run-similarity">
            <CirclePlus size={17} />
            <span>Add Compound</span>
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
              <Target size={16} /> Target Compounds (To be Compared) :
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
          </div>
        </div>
      </section>

      {similarity_data.similarity_results.length > 0 && (
        <Similarity 
          reference_compound={similarity_data.compound}
          similarity_results={similarity_data.similarity_results}
        />
      )}
    </main>
  );
};

export default SimilarityAnalysis;
