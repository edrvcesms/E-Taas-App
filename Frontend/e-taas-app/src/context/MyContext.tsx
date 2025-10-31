
import { createContext, useContext, useState } from "react";
import type{ ContextType } from "../types/ContextTypes";


export const AppContext = createContext<ContextType | null>(null);

export const MyProvider: React.FC<{children: React.ReactNode}> = ({children}) => {

  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  return(
    <>
      <AppContext.Provider value={{isAuthenticated, setIsAuthenticated}}>
        {children}
      </AppContext.Provider>
    </>
  );
}

export const useMyContext = () => {
  const context = useContext(AppContext);
  if(!context) throw new Error("Invalid Context");
  return context;
}