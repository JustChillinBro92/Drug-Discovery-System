import {
  Brackets,
  CheckSquare,
  Circle,
  Filter,
  Search,
  X,
  ListOrdered,
  ArrowDownCircle,
  Sparkles,
  Brain,
  ScrollText,
  BookOpenText,
  Cpu,
  SendHorizontal,
  BadgeCheck,
  Dot,
  Paperclip,
  Lightbulb,
  MessageSquare 
} from 'lucide-react';

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
            <Cpu size={13} style={{ color: "#0649db" }} /> Qdrant HNSW-Dense
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
            <Brain className="assistant-brain-icon" size={30} />
            <div>
              <div className="assistant-title-row">
                <h3>Literature AI Research Assistant</h3>
                <span className="synthesis-badge">RETRIEVAL AGENT</span>
              </div>
              <p className="assistant-subtitle">
                Live cross-examination &amp; semantic inference over 24 grounded studies (412 chunks)
              </p>
            </div>
          </div>
          <div className="chatbox-header-right">
            <span><Dot size={20} />24 Grounded Papers Active</span>
          </div>
        </div>

        <div className="chatbox-body">
          <div className="assistant-sparkle-icon"><Sparkles size={15} className="sparkle  "/></div>
          <div className="chatbox-output">
            <p>
              I have synthesized the <strong>24 indexed publications</strong> regarding 
              <strong> Aspirin platelet aggregation &amp; COX-1 inhibition. </strong> 
              Across 412 retrieved semantic vector chunks, consensus confirms irreversible 
              acetylation of <strong className="highlighted-term">Ser529</strong> in the 
              platelet COX-1 catalytic pocket, resulting in ~100% suppression of platelet 
              thromboxane A2 (TXA2) within 60 minutes.
            </p>
            <div className="chatbox-output-footer">
              <Paperclip size={14} />
              <strong>PRIMARY CITATIONS:</strong>
              <span>PMID: 25164478</span>
              <Dot size={16} />
              <span>PMC4389211</span>
              <Dot size={16} />
              <span>NEJM: 379(12)</span>
            </div>
          </div>
        </div>

        <div className="chatbox-footer">
          <Lightbulb size={15} />
          <strong>SUGGESTED INQUIRIES:</strong>
          <button type="button">Summarize off-target effects &amp; gastric toxicity</button>
          <button type="button">Compare COX-1 vs COX-2 selectivity profile</button>
          <button type="button">Extract clinical low-dose regimens</button>
        </div>

        <div className="questionBox">
          <MessageSquare size={19} />
          <input
            type="text"
            placeholder="Ask a question about the retrieved literature, synthesize findings, or compare mechanisms..."
            aria-label="Ask a question about the retrieved literature"
          />
          <button type="button">
            INQUIRE
            <SendHorizontal size={15} />
          </button>
        </div>
      </section>
    </main>
  );
};

export default LiteratureRetrieval;