import { useCurrentUser } from "../store/currentUserStore";
import { Navigate, Outlet } from "react-router-dom";


export const AuthLayout: React.FC = () => {

  const currentUser = useCurrentUser((state) => state.currentUser);

  if (currentUser) return <Navigate to="/" replace />;
  
  return <Outlet />;
};