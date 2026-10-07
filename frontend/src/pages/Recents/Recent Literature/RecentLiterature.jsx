import { useMemo, useState } from "react";
import { Plus, ExternalLink, Search } from "lucide-react";

import data from "../../../assets/data";

import "./RecentLiterature.css";

const getPaperId = (paper) => paper.pmid || paper.pmcid || paper.doi;
const papers = Object.entries(data.state.literature_retrievals).flatMap(
  ([retrievalId, retrieval]) => retrieval.referenced_papers,
);

const RecentLiterature = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("recent");

  const visiblePapers = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();

    const filteredPapers = papers
      .map((paper) => {
        if (!normalizedQuery) {
          return {
            paper,
            searchScore: 0,
          };
        }

        const title = paper.title?.toLowerCase() || "";

        const text = [
          paper.title,
          paper.doi,
          paper.pmid,
          paper.pmcid,
          paper.journal,
          ...paper.authors,
          ...paper.keywords,
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();

        if (title.startsWith(normalizedQuery)) {
          return {
            paper,
            searchScore: 2,
          };
        }

        if (text.includes(normalizedQuery)) {
          return {
            paper,
            searchScore: 1,
          };
        }

        return null;
      })
      .filter(Boolean);

    return filteredPapers
      .sort((a, b) => {
        // Search relevance first
        if (normalizedQuery && a.searchScore !== b.searchScore) {
          return b.searchScore - a.searchScore;
        }

        // Then user's selected sorting
        if (sortBy === "title")
          return a.paper.title.localeCompare(b.paper.title);
        if (sortBy === "journal")
          return a.paper.journal.localeCompare(b.paper.journal);
        if (sortBy === "year")
          return a.paper.publication_year - b.paper.publication_year;
        if (sortBy === "paperId")
          return getPaperId(a.paper).localeCompare(getPaperId(b.paper));
        if (sortBy === "author")
          return a.paper.authors[0].localeCompare(b.paper.authors[0]);
        if (sortBy === "keywords")
          return a.paper.keywords[0].localeCompare(b.paper.keywords[0]);
      })
      .map(({ paper }) => paper);
  }, [papers, searchQuery, sortBy]);

  return (
    <main className="recent-literature">
      {/* 1st section tag */}

      <section className="recent-literature-card">
        <div className="literature-content">
          <div className="literature-heading">
            <div>
              <div className="literature-route">
                <span>KNOWLEDGE DISCOVERY</span>
                <span>/</span>
                <strong>RECENT RETRIEVALS</strong>
              </div>
              <h1>Recent Literature Registry</h1>
              <p>
                Peer-reviewed research and validated molecular evidence
                supporting active drug discovery targets.
              </p>
            </div>

            <div className="literature-actions">
              <button type="button" className="literature-new-button">
                <Plus size={18} />
                Fetch New Literature
              </button>
            </div>
          </div>

          <div className="literature-toolbar">
            <label className="literature-search">
              <Search size={18} aria-hidden="true" />
              <input
                type="search"
                placeholder="Search papers by title, author, DOI, or target..."
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
              />
            </label>

            <label className="literature-sort">
              <span>SORT :</span>
              <select
                value={sortBy}
                onChange={(event) => setSortBy(event.target.value)}
              >
                <option value="recent">Recently Added</option>
                <option value="title">Title</option>
                <option value="journal">Journal</option>
                <option value="year">Publication Year</option>
                <option value="paperId">Paper ID</option>
                <option value="author">Author</option>
                <option value="keywords">Keywords</option>
              </select>
            </label>
          </div>
        </div>
      </section>

      {/* 2nd section tag */}
      <section
        className="recent-literature-papers"
        aria-label="Literature papers"
      >
        {visiblePapers.map((paper) => {
          const paperId = getPaperId(paper);
          const paperUrl =
            paper.url || `https://europepmc.org/article/MED/${paper.pmid}`;

          return (
            <article className="literature-paper" key={paperId}>
              <div className="literature-paper-content">
                <div className="literature-paper-meta">
                  <strong>{paper.journal}</strong>
                  <span className="paper-meta-separator">•</span>
                  <span>{paper.publication_year}</span>
                  <span className="paper-meta-separator">•</span>
                  {paper.pmcid && (
                    <span className="paper-pmid">
                      {paper.pmid ? `PMCID : ${paper.pmcid}` : paperId}
                    </span>
                  )}
                  {paper.pmid && (
                    <span className="paper-pmid">
                      {paper.pmid ? `PMID : ${paper.pmid}` : paperId}
                    </span>
                  )}
                  {paper.doi && (
                    <span className="paper-pmid">
                      {paper.pmid ? `DOI : ${paper.doi}` : paperId}
                    </span>
                  )}
                  <span className="paper-grounded">
                    <i />
                    Grounded
                  </span>
                </div>

                <h2 className="literature-paper-title">{paper.title}</h2>

                <div>
                  <div className="paper-detail-row">
                    <span className="paper-detail-label">Authors:</span>
                    <div className="paper-tags">
                      {paper.authors.map((author) => (
                        <span className="paper-tag paper-author" key={author}>
                          {author}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="paper-detail-row">
                    <span className="paper-detail-label">Keywords:</span>
                    <div className="paper-tags">
                      {paper.keywords.map((keyword) => (
                        <span className="paper-tag" key={keyword}>
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="literature-paper-actions">
                <a
                  className="paper-europe-pmc"
                  href={paperUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Europe PMC
                  <ExternalLink size={12} />
                </a>
                <a
                  className="paper-view-button"
                  href={paperUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  View Paper
                  <ExternalLink size={12} />
                </a>
              </div>
            </article>
          );
        })}
      </section>
    </main>
  );
};

export default RecentLiterature;
