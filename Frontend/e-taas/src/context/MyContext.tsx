import { createContext, useContext } from "react";
import type { ReactNode } from "react";
import React from "react";
import { useState } from "react";

interface MyContextType {
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const MyContext = createContext<MyContextType | undefined>(undefined);

interface MyContextProviderProps {
  children: ReactNode;
}

export const MyContextProvider = ({ children }: MyContextProviderProps) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  return (
    <MyContext.Provider value={{ isLoading, setIsLoading}}>
      {children}
    </MyContext.Provider>
  );
};

export const useMyContext = (): MyContextType => {
  const context = useContext(MyContext);

  if (!context) {
    throw new Error("useMyContext must be used within MyContextProvider");
  }

  return context;
};