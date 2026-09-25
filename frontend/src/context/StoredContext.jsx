import axios from "axios";
import { createContext, useEffect, useState } from "react";

export const StoreContext = createContext(null);

const StoreContextProvider = (props) => {
  const url = "http://localhost:8000";

  const [token, setToken] = useState("");

  const handleAuthError = () => {
    localStorage.removeItem("token");
    setToken("");
  };

  const contextValues = {
    url,
    token,
    setToken,
  };

  return (
    <StoreContext.Provider value={contextValues}>
      {props.children}
    </StoreContext.Provider>
  );
};

export default StoreContextProvider;
