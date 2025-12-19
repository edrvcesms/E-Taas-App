import { Navigate, Outlet } from "react-router-dom";
import { useCurrentUser } from "../store/currentUserStore";
import React from "react";


export const UserProtectedRoutes: React.FC = () => {
  const currentUser = useCurrentUser((state) => state.currentUser);

  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}