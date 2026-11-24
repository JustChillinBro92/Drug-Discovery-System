import { useContext, useEffect, useRef, useState } from "react";
import {
  ArrowLeft,
  Bot,
  CircleAlert,
  CircleFadingPlus,
  Plus,
  RotateCw,
  Send,
  Sparkles,
} from "lucide-react";

import "../Compound Analysis/CompoundAnalysis.css";
import "./Assistant.css";
import { StoreContext } from "../../context/StoredContext";

const Assistant = () => {
  const { backendUrl, ensureConversation, clearConversation } = useContext(StoreContext);
  const [assistantActive, setAssistantActive] = useState(
    () => sessionStorage.getItem("drug-discovery-assistant-active") === "true",
  );
  const [messages, setMessages] = useState(() => {
    if (
      sessionStorage.getItem("drug-discovery-assistant-active") !== "true"
    ) {
      return [];
    }

    try {
      return JSON.parse(
        sessionStorage.getItem("drug-discovery-assistant-messages"),
      ) || [];
    } catch {
      return [];
    }
  });
  const [hasStoredSession, setHasStoredSession] = useState(() => {
    const conversationId = sessionStorage.getItem(
      "drug-discovery-conversation-id",
    );
    const storedMessages = sessionStorage.getItem(
      "drug-discovery-assistant-messages",
    );

    if (!conversationId || !storedMessages) return false;

    try {
      return JSON.parse(storedMessages).length > 0;
    } catch {
      return false;
    }
  });
  const [query, setQuery] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const messagesRef = useRef(null);

  const hasMessages = assistantActive && messages.length > 0;

  useEffect(() => {
    if (messages.length > 0) {
      sessionStorage.setItem(
        "drug-discovery-assistant-messages",
        JSON.stringify(messages),
      );
    }
  }, [messages]);

  useEffect(() => {
    sessionStorage.setItem(
      "drug-discovery-assistant-active",
      String(assistantActive),
    );
  }, [assistantActive]);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages, isSending]);

  const handleSend = async () => {
    const trimmedQuery = query.trim();
    if (!trimmedQuery || isSending) return;

    setError("");
    setIsSending(true);

    let activeConversationId;

    try {
      activeConversationId = await ensureConversation();
    } catch (sessionError) {
      setError(
        sessionError instanceof TypeError
          ? "Cannot reach the backend!"
          : sessionError.message,
      );
      setIsSending(false);
      return;
    }

    setQuery("");
    setAssistantActive(true);
    setMessages((currentMessages) => [
      ...currentMessages,
      { role: "user", text: trimmedQuery },
    ]);

    try {
      const response = await fetch(`${backendUrl}/c/${activeConversationId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmedQuery }),
      });

      if (!response.ok) {
        throw new Error("The assistant could not process that request.");
      }

      const result = await response.json();
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: "assistant",
          text: result.message || "No response was returned.",
        },
      ]);
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? "Cannot reach the backend!"
          : requestError.message,
      );
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleResumeSession = () => {
    try {
      const storedMessages = JSON.parse(
        sessionStorage.getItem("drug-discovery-assistant-messages"),
      );

      if (Array.isArray(storedMessages) && storedMessages.length > 0) {
        setMessages(storedMessages);
        setAssistantActive(true);
        setHasStoredSession(false);
      }
    } catch {
      setError("Unable to restore the previous session.");
    }
  };

  const handleClearSession = async () => {
    setError("");
    setMessages([]);
    setQuery("");
    setAssistantActive(false);
    setHasStoredSession(false);
    sessionStorage.removeItem("drug-discovery-assistant-active");
    sessionStorage.removeItem("drug-discovery-assistant-messages");

    try {
      await clearConversation();
    } catch (sessionError) {
      setError(
        sessionError instanceof TypeError
          ? "Cannot reach the backend!"
          : sessionError.message,
      );
    }
  };

  const handleBackToDefault = () => {
    setHasStoredSession(messages.length > 0);
    setAssistantActive(false);
  };

  return (
    <main
      className={`compound-analysis assistant-analysis ${hasMessages ? "chat-active" : ""}`}
    >
      <header className="compound-card assistant-card">
        <div className="compound-header">
          <div>
            <div className="route">
              <span>MAIN CONSOLE</span>
              <span>/</span>
              <strong>AI ASSISTANT</strong>
            </div>
            <h1>Research Assistant</h1>
            <p>
              Ask questions and explore evidence across your research session.
            </p>
          </div>

          <div className="new-session">
            <button type="button" onClick={handleClearSession}>
              <CircleFadingPlus size={17} />
              Clear Session
            </button>
          </div>
        </div>
      </header>

      <section className="assistant-workspace compound-card">
        {hasMessages && (
          <button
            type="button"
            className="assistant-back"
            onClick={handleBackToDefault}
            aria-label="Back to assistant welcome"
          >
            <ArrowLeft size={18} />
          </button>
        )}
        {!hasMessages ? (
          <div className="assistant-empty-state">
            <div className="assistant-mark">
              <Bot size={28} />
            </div>
            <p className="eyebrow">DRUG DISCOVERY AI</p>
            <h2>How can I assist your research?</h2>
            <p className="empty-description">
              Ask about compounds, biomedical literature, targets, potential
              side effects or treatable diseases.
            </p>
            {hasStoredSession && (
              <button
                type="button"
                className="resume-session"
                onClick={handleResumeSession}
              >
                <RotateCw size={16} />
                Resume last session
              </button>
            )}
          </div>
        ) : (
          <div className="assistant-messages" ref={messagesRef}>
            <div className="message-list">
              {messages.map((message, index) => (
                <article
                  className={`assistant-message ${message.role}`}
                  key={`${message.role}-${index}`}
                >
                  {message.role === "assistant" && (
                    <div className="message-icon">
                      <Sparkles size={16} />
                    </div>
                  )}
                  <div className="message-content">
                    <span className="message-label">
                      {message.role === "user" ? "YOU" : "RESEARCH ASSISTANT"}
                    </span>
                    <p>{message.text}</p>
                  </div>
                </article>
              ))}
              {isSending && (
                <article className="assistant-message assistant">
                  <div className="message-icon">
                    <Sparkles size={16} />
                  </div>
                  <div className="message-content">
                    <span className="message-label">RESEARCH ASSISTANT</span>
                    <p className="typing-indicator">
                      Analyzing your request...
                    </p>
                  </div>
                </article>
              )}
            </div>
          </div>
        )}

        <div className="assistant-composer">
          {error && (
            <div className="assistant-error" role="alert">
              <CircleAlert size={16} />
              <span>{error}</span>
            </div>
          )}
          <div className="composer-box">
            <button
              type="button"
              className="composer-add"
              aria-label="Add context"
            >
              <Plus size={18} />
            </button>
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a research question..."
              rows={1}
              disabled={isSending}
              aria-label="Research question"
            />
            <button
              type="button"
              className="send-button"
              onClick={handleSend}
              disabled={!query.trim() || isSending}
              aria-label="Send message"
            >
              <Send size={17} />
            </button>
          </div>
          <p className="composer-note">
            AI-generated results should be verified against original sources.
          </p>
        </div>
      </section>
    </main>
  );
};

export default Assistant;
