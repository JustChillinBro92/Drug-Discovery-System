import { createContext, useCallback, useState } from "react";

export const StoreContext = createContext(null);

const StoreContextProvider = (props) => {
  // const url = "http://localhost:8000";
  const url = "https://www.ebi.ac.uk/chembl/api/data/"
  const backendUrl = "http://127.0.0.1:8000";
  const conversationStorageKey = "drug-discovery-conversation-id";

  const [token, setToken] = useState("");
  const [conversationId, setConversationId] = useState(
    () => sessionStorage.getItem(conversationStorageKey)
  );

  const ensureConversation = useCallback(async () => {
    const storedId = sessionStorage.getItem(conversationStorageKey);
    if (storedId) {
      setConversationId(storedId);
      return storedId;
    }

    const response = await fetch(`${backendUrl}/sessions`, {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error("Unable to start a conversation.");
    }

    const session = await response.json();
    sessionStorage.setItem(conversationStorageKey, session.conversation_id);
    setConversationId(session.conversation_id);
    return session.conversation_id;
  }, []);

  const clearConversation = useCallback(async () => {
    if (conversationId) {
      await fetch(`${backendUrl}/c/${conversationId}/clear`, {
        method: "POST",
      });
    }

    sessionStorage.removeItem(conversationStorageKey);
    setConversationId(null);
  }, [conversationId]);

  const contextValues = {
    url,
    backendUrl,
    token,
    setToken,
    conversationId,
    setConversationId,
    ensureConversation,
    clearConversation,
  };

  return (
    <StoreContext.Provider value={contextValues}>
      {props.children}
    </StoreContext.Provider>
  );
};

export default StoreContextProvider;
