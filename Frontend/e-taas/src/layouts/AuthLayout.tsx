import { useCurrentUser } from "../store/currentUserStore";
import { Navigate, Outlet } from "react-router-dom";


export const AuthLayout: React.FC = () => {

  const currentUser = useCurrentUser();

  if (currentUser) return <Navigate to="/" replace />;
  
  return <Outlet />;
};