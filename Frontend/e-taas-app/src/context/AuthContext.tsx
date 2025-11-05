import React, { createContext, useContext, useState } from 'react'
import type { User } from '../types/User';

export const AuthContext = createContext<any | null>(null);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {

  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, user, setUser, isLoading, setIsLoading}}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  return useContext(AuthContext);
}
