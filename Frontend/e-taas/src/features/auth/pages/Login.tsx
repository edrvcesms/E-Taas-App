import React from "react";
import { LoginForm } from "../components/LoginForm";

export const Login: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 via-pink-50 to-gray-50">
      <div className="w-full max-w-xl">
        <LoginForm />
      </div>
    </div>
  );
};