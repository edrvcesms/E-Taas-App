export interface ContextType{
  isAuthenticated: boolean | null;
  setIsAuthenticated: (isAuthenticated:boolean) => void;
}