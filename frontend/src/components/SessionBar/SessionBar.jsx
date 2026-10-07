import { useState } from "react";

import {
  Atom,
  Germ,
  Dna,
  TriangleAlert,
  ScrollText,
  PanelLeftOpen,
  MonitorDot,
  NotebookText,
  CalendarDays,
  ListChevronsUpDown,
  ListChevronsDownUp,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

import CollapsedSessionbar from "./CollapsedSessionbar";

import "./Sessionbar.css";

import data from "../../assets/data";

const Sessionbar = () => {
  const [closeSessionPanel, setCloseSessionPanel] = useState(false);
  const [expandedItems, setExpandedItems] = useState(new Set());

  const toggleCompound = (id) => {
    setExpandedItems((prev) => {
      const updated = new Set(prev);

      if (updated.has(id)) updated.delete(id);
      else updated.add(id);

      return updated;
    });
  };

  const getId = (paper) => {
    if (paper.pmcid) return paper.pmcid;
    if (paper.pmid) return paper.pmid;
    if (paper.doi) return paper.doi;
  };

  const getIdType = (id) => {
    if (/^PMC\d+$/.test(id)) return "PMCID";
    if (/^\d+$/.test(id)) return "PMID";
    if (/^10\.\d{4,9}\/\S+$/.test(id)) return "DOI";

    return "Unknown";
  };

  const sessionPanelAction = () => {
    setCloseSessionPanel(!closeSessionPanel);
  };

  return !closeSessionPanel ? (
    <div className="sessionbar">
      <div className="title-container">
        <div className="title">
          <h2>
            Current
            <MonitorDot className="monitor" />
          </h2>
          <h2 style={{ fontSize: "22px" }}>Research Session</h2>
          <h3>Contextual Evidence</h3>
        </div>
        <div className="panel-close">
          <PanelLeftOpen size={24} onClick={sessionPanelAction} />
        </div>
      </div>

      <div className="navigations-container">
        <div className="navigations">
          <div className="navigation-divider" aria-hidden="true" />
          <ul className="compounds">
            <span>
              <Atom size={16} />
              <h4>Active Compounds</h4>
              <p className="qty">{data.state.analyzed_compounds.length}</p>
              <ListChevronsUpDown className="icon" size={22} />
            </span>
            <div className="session-items">
              {data.state.analyzed_compounds.map((compound) => {
                const compoundData = compound.compound_details.compound;
                const isExpanded = expandedItems.has(compoundData.chembl_id);

                return (
                  <li
                    key={compoundData.chembl_id}
                    onClick={() => toggleCompound(compoundData.chembl_id)}
                  >
                    <div className="compound">
                      <p>{compoundData.canonical_name}</p>
                      {isExpanded ? (
                        <ChevronUp size={20} />
                      ) : (
                        <ChevronDown size={20} />
                      )}
                    </div>

                    {isExpanded && (
                      <div className="summary">
                        <span>
                          <Dna size={16} />
                          <h5>Target Proteins</h5>
                          <p className="qty">
                            {compound.summary.protein_count}
                          </p>
                        </span>
                        <span>
                          <TriangleAlert size={16} />
                          <h5>Potential Side Effects</h5>
                          <p className="qty">
                            {compound.summary.side_effect_count}
                          </p>
                        </span>
                        <span>
                          <Germ size={16} />
                          <h5>Treatable Diseases</h5>
                          <p className="qty">
                            {compound.summary.treatable_disease_count}
                          </p>
                        </span>
                      </div>
                    )}
                  </li>
                );
              })}
            </div>
          </ul>

          <ul className="papers">
            <span>
              <ScrollText size={16} />
              <h4>Referenced Papers</h4>
              <p className="qty">{data.state.referenced_paper_ids.length}</p>
              <ListChevronsUpDown className="icon" size={22} />
            </span>
            <div className="session-items">
              {Object.entries(data.state.literature_retrievals).flatMap(
                ([retrievalId, retrieval]) =>
                  retrieval.referenced_papers.map((paper) => {
                    const paper_id = getId(paper);
                    const isExpanded = expandedItems.has(paper_id);

                    return (
                      <li
                        key={paper_id}
                        onClick={() => toggleCompound(paper_id)}
                      >
                        <div className="compound">
                          <div className="id">
                            <h5>{getIdType(paper_id)}:</h5>
                            <p>{paper_id}</p>
                          </div>
                          {isExpanded ? (
                            <ChevronUp size={20} />
                          ) : (
                            <ChevronDown size={20} />
                          )}
                        </div>

                        {isExpanded && (
                          <div className="paper-summary">
                            <span>
                              <NotebookText size={11} />
                              <h5>Journal:</h5>
                              <p className="desc">{paper.journal}</p>
                            </span>
                            <span>
                              <CalendarDays size={11} />
                              <h5>Year:</h5>
                              <p className="desc year">
                                {paper.publication_year}
                              </p>
                            </span>
                          </div>
                        )}
                      </li>
                    );
                  }),
              )}
            </div>
          </ul>
        </div>
      </div>
    </div>
  ) : (
    <CollapsedSessionbar sessionPanelAction={sessionPanelAction} />
  );
};

export default Sessionbar;
