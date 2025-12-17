import React from "react";
import type { LoginData } from "../../../types/auth/Login";
import { useForm } from "../../../hooks/useForm";
import { useCurrentUser } from "../../../store/currentUserStore";
import { loginUser } from "../../../services/auth/LoginService";
import { useNavigate } from "react-router-dom";

export const LoginForm: React.FC = () => {
  const { values, handleChange, reset } = useForm<LoginData>({
    email: "",
    password: "",
  });

  const navigate = useNavigate();
  const { currentUser, setCurrentUser } = useCurrentUser();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const user = await loginUser(values);
      setCurrentUser(user);
      navigate("/");
      reset();
    } catch (error) {
      alert("Login failed. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Email</label>
        <input
          type="email"
          name="email"
          value={values.email}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
          placeholder="Enter your email"
        />
      </div>

      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Password</label>
        <input
          type="password"
          name="password"
          value={values.password}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
          placeholder="Enter your password"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold"
      >
        Log In
      </button>
    </form>
  );
};
