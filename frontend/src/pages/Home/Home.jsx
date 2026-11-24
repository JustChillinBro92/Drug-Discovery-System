import "./Home.css";

import {
  RotateCwClock,
  CircleFadingPlus,
  Search,
  Bot,
  BookOpenText,
  Microscope,
  FolderOpen,
  X,
  SquareArrowOutUpRight,
} from "lucide-react";

const Home = () => {
  return (
    <main className="compound-analysis literature-analysis">
      <header className="compound-card literature-card">
        <div className="compound-header">
          <div>
            <div className="route">
              <span>MAIN CONSOLE</span>
              <span>/</span>
              <strong>DASHBOARD</strong>
            </div>
            <h1>Welcome Back, Dr. Rostova</h1>
            <p>
              What is on our agenda today? You can resume your last session or
              start a new one.
            </p>
          </div>

          {/* <div className="new-session">
            <button type="button">
              <CircleFadingPlus size={17} />
              New Session
            </button>
          </div> */}
        </div>
      </header>

      <section className="aggregation-card session-card">
        <div className="session-header">
          <div className="session-state">
            <h4>
              <RotateCwClock size={14}/>
              IN PROGRESS
            </h4>
          </div>
          <div className="session-id">
            SESSION ID : <p>9f8eaa74-f559-4898-8f2b-ff1e8916ccc</p>
          </div>
        </div>

        <div className="session">
          <div className="details">
            <div className="research-topic">
              <h2>Aspirin platelet aggregation and COX-1 inhibition</h2>
            </div>

            <div className="state">
              <div className="items">
                <h4>
                  ACTIVE
                  <br />
                  COMPOUNDS
                </h4>
                <h3>12</h3>
                <h5>3 Lipinski Cleared</h5>
              </div>
              <div className="items">
                <h4>
                  CITED
                  <br />
                  PAPERS
                </h4>
                <h3>45</h3>
                <h5>Sources</h5>
              </div>
              <div className="items">
                <h4>
                  VECTOR
                  <br />
                  CHUNKS
                </h4>
                <h3>1240</h3>
                <h5>Chunks</h5>
              </div>
              <div className="items">
                <h4>
                  REFERENCED
                  <br />
                  CHUNKS
                </h4>
                <h3>500</h3>
                <h5>Chunks</h5>
              </div>
            </div>
          </div>

          <div className="navs">
            <button type="button">
              <Bot size={17} />
              Resume Agent Mode
            </button>
            <button type="button">
              <BookOpenText size={17} />
              Retrieve Literature
            </button>
            <button type="button">
              <Microscope size={17} />
              Analyze Compounds
            </button>
          </div>
        </div>
      </section>

      <section className="past-sessions-card recent-compounds-card">
        <div className="past-sessions-header compounds-heading">
          <div className="header compounds-title">
            <FolderOpen size={18} color="#0649db" />
            <h4>Recent Sessions</h4>
            <span>3 of 120</span>
          </div>

          <div className="search compound-input">
            <Search size={17} />
            <input type="text" placeholder="Filter Sessions" />
            <button type="button" className="clear-input">
              <X size={17} />
            </button>
          </div>
        </div>

        <div className="session-headings grid-headings">
          <p>SESSION TITLE & ID</p>
          <p>COMPOUNDS</p>
          <p>CITED PAPERS</p>
          <p>VECTOR CHUNKS</p>
          <p>REF. CHUNKS</p>
          <p>ACTIONS</p>
        </div>

        <div className="session-list list">
          <div className="list-item">
            <div className="item">
              <h5>Aspirin platelet aggregation and COX-1 inhibition</h5>
              <h3>ID: 9f8eaa74-f559-4898-8f2b-ff1e8916ccc</h3>
            </div>
            <div className="item">
              <h5>12</h5>
              <h3>structures</h3>
            </div>
            <div className="item">
              <h5>45</h5>
              <h3>sources</h3>
            </div>
            <div className="item">
              <h5>1240</h5>
              <h3>chunks</h3>
            </div>
            <div className="item">
              <h5>500</h5>
              <h3>chunks</h3>
            </div>
            <div className="item">
              <span className="view">
                <h3>View</h3>
                <SquareArrowOutUpRight size={12} />
              </span>
            </div>
          </div>

          <div className="list-item">
            <div className="item">
              <h5>Aspirin platelet aggregation and COX-1 inhibition</h5>
              <h3>ID: 9f8eaa74-f559-4898-8f2b-ff1e8916ccc</h3>
            </div>
            <div className="item">
              <h5>12</h5>
              <h3>structures</h3>
            </div>
            <div className="item">
              <h5>45</h5>
              <h3>sources</h3>
            </div>
            <div className="item">
              <h5>1240</h5>
              <h3>chunks</h3>
            </div>
            <div className="item">
              <h5>500</h5>
              <h3>chunks</h3>
            </div>
            <div className="item">
              <span className="view">
                <h3>View</h3>
                <SquareArrowOutUpRight size={12} />
              </span>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
  ``;
};

export default Home;
