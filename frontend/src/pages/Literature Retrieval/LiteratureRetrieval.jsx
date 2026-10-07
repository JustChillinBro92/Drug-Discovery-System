import {
  Brackets,
  CheckSquare,
  Circle,
  Filter,
  Search,
  X,
  ListOrdered,
  ArrowDownCircle,
  Microscope,
  Sparkles,
  Brain,
  ScrollText,
  BookOpenText,
  Cpu,
  MessageSquareText,
  Link2,
  SendHorizontal,
  BadgeCheck,
  RotateCw,
  Dot,
  Paperclip,
  Lightbulb,
  MessageSquare 
} from 'lucide-react';
import { useState } from 'react';
import './LiteratureRetrieval.css';

const queryPresets = [
  'Aspirin COX-1',
  'Cancer Immunotherapy PD-L1',
  'EGFR T790M Resistance',
  'KRAS G12D Scaffolds',
  'Ibuprofen vs Acetaminophen',
];

const LiteratureRetrieval = () => {
  return (
    <main className="compound-analysis literature-analysis">
      <section className="compound-card literature-card">
        <div className="compound-header">
          <div>
            <div className="route">
              <span>KNOWLEDGE DISCOVERY</span>
              <span>/</span>
              <strong>LITERATURE RETRIEVAL</strong>
            </div>
            <h1>Literature Acquisition &amp; Semantic RAG Engine</h1>
            <p>
              Retrieve literature, compute semantic chunk embeddings,
              and inspect citation-grounded evidence. Connected to Europe PMC.
            </p>
          </div>

          <div className="engine-ready">
            <ScrollText size={17} />
            <span>Engine Ready</span>
          </div>
        </div>

        <form className="analysis-form literature-form">
          <div className="compound-input literature-input">
            <Search size={18} />
            <input
              type="text"
              placeholder="Aspirin platelet aggregation and COX-1 inhibition"
            />
            <button type="button" className="clear-input">
              <X size={17} />
            </button>
          </div>

          <div className="max-papers-box" aria-label="Maximum papers selector">
            <ListOrdered size={16} />
            <div className="max-papers-meta">
              <span className="meta-label">MAX PAPERS</span>
              <input className="meta-value"
                type="number"
                min="1"
                placeholder="100"
              />
            </div>
          </div>

          <button type="submit" className="run-analysis fetch-button">
            <ArrowDownCircle size={17} />
            <span>Fetch Papers</span>
          </button>
        </form>

        <div className="quick-samples literature-presets">
          <span className="quick-samples-label">Query Presets:</span>
          {queryPresets.map((preset) => (
            <button key={preset} type="button" className="sample">
              {preset}
            </button>
          ))}
        </div>

        <div className="analyzed-compounds literature-pipeline">
          <div className="literature-pipeline-row">
            <span className="pipeline-label">
              <Circle size={8} fill="currentColor" /> PIPELINE:
            </span>
            <span className="pipeline-metric">
              <BookOpenText size={14} /> 24 Papers Retrieved
            </span>
            <span className="pipeline-metric">
              <CheckSquare size={14} /> 18 Newly Indexed
            </span>
            <span className="pipeline-metric">
              <Filter size={14} /> 6 Duplicates Filtered
            </span>
            <span className="pipeline-metric pipeline-chunks">
              <Brackets size={14} /> 412 Chunks Added
            </span>
          </div>
        </div>

        <div className="vector-row literature-vector-row">
          <span className="vector-item">
            <Cpu size={13} style={{ color: "0649db" }} /> Qdrant HNSW-Dense
          </span>
          <span className="vector-separator">•</span>
          <span className="vector-item">Metric : Cosine</span>
          <span className="vector-separator">•</span>
          <label className="vector-item k-value">
            Top k papers :
            <input
              type="number"
              min="1"
              placeholder="5"
            />
          </label>
        </div>
      </section>


      <section className="aggregation-card">
        <div className="aggregation-header">
          <h2>Aspirin platelet aggregation and COX-1 inhibition <br /> [Synthesis & Vector Retrieval]</h2>
          <div className="grounded">
            <BadgeCheck size={17} style={{ color: "#047857" }} />
            <span>GROUNDED & INDEXED</span>
          </div>
        </div>
      </section>


      <section className="chatbox-card">
        <div className="chatbox-header">
          <div className="chatbox-header-left">
            <Brain size={30} style={{ backgroundColor: "D9E1F3", padding: "5px", color: "blue" }} />
            <h3>Literature AI Research Assistant</h3>
          </div>
          <div className="chatbox-header-right">

            <span>24 Grounded Papers Active</span>
            <RotateCw size={17} />
          </div>
        </div>
        <div className="chatbox-body">
          <Sparkles size={30} style={{ backgroundColor: "#0040e0", color: "white", padding: "5px", borderRadius: "10px" }} />
          <div className='chatbox-output'>

            I have synthesized the 24 indexed publications regarding Aspirin platelet aggregation & COX-1 inhibition. Across 412 retrieved semantic vector chunks, consensus confirms irreversible acetylation of Ser529 in the platelet COX-1 catalytic pocket, resulting in ~100% suppression of platelet thromboxane A2 (TXA2) within 60 minutes.

            Would you like to examine downstream prostacyclin (PGI2) sparing mechanisms, evaluate clinical low-dose protocols (75–100 mg), or compare binding kinetics against reversible nonselective NSAIDs?

            <div className='chatbox-output-footer'>
              <Paperclip size={20} />
              <p>PRIMARY CITATIONS:    </p>
              <span>PMID: 25164478</span>
              <Dot />
              <span>PMC4389211</span>
              <Dot />
              <span>NEJM: 379(12)</span>
            </div>

          </div>
        </div>

        <div className='chatbox-footer'>
          <Lightbulb style={{ color: "0040e0" }} />
          <p>SUGGESTED INQUIRIES:  </p>
          <span>opt1</span>
          <span>opt2</span>
        </div>

        <div className='questionBox'>
          <p>Ask your AI Assisstant</p>
          <button>
            Inquire
          </button>
        </div>

      </section>


    </main>
  );
};

export default LiteratureRetrieval;