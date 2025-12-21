import React, { useState } from "react";
import type { LoginData } from "../../../types/auth/Login";
import { useForm } from "../../../hooks/general/useForm";
import { useCurrentUser } from "../../../store/currentUserStore";
import { loginUser } from "../../../services/auth/LoginService";
import { useMyContext } from "../../../context/MyContext";
import { useNavigate } from "react-router-dom";
import { Mail, Lock, Eye, EyeOff } from "lucide-react";

export const LoginForm: React.FC = () => {
  const { values, handleChange, reset } = useForm<LoginData>({
    email: "",
    password: "",
  });

  const navigate = useNavigate();
  const { setCurrentUser } = useCurrentUser();
  const { isLoading, setIsLoading } = useMyContext();
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const user = await loginUser(values);
      setCurrentUser(user);
      navigate("/");
      reset();
    } catch (err: any) {
      console.log(err.response.data.detail);
      setError(err.response?.data?.detail || "An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-pink-500">Welcome Back</h1>
          <p className="text-gray-600">Sign in to continue to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Email Input */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
              <input
                type="email"
                name="email"
                id="email"
                value={values.email}
                onChange={handleChange}
                placeholder="you@example.com"
                required
                className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent focus:bg-white transition-all outline-none"
              />
            </div>
          </div>

          {/* Password Input */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                id="password"
                value={values.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
                className="w-full pl-12 pr-12 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent focus:bg-white transition-all outline-none"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                {showPassword ? (
                  <EyeOff className="w-5 h-5" />
                ) : (
                  <Eye className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>

          {/* Forgot Password Link */}
          <div className="flex justify-end">
            <button
              type="button"
              onClick={() => navigate("/forgot-password")}
              className="text-sm text-pink-500 hover:text-pink-600 font-medium transition-colors"
            >
              Forgot password?
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm flex items-start gap-2">
              <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span>{error}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white font-semibold py-3.5 rounded-xl transition-all duration-300 transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-lg shadow-pink-500/30"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Logging in...
              </span>
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-gray-200">
        <p className="text-center text-gray-500 text-sm">
          By signing up, you agree to our
          <button
            type="button"
            onClick={() => navigate("/terms")}
            className="text-pink-600 hover:underline mx-1"
          >
            Terms of Service
          </button>
          and
          <button
            type="button"
            onClick={() => navigate("/privacy")}
            className="text-pink-600 hover:underline mx-1"
          >
            Privacy Policy
          </button>
        </p>
      </div>

        

        {/* Register Link */}
        <div className="text-center text-sm text-gray-600 pt-4 border-t border-gray-100">
          Don't have an account?{" "}
          <button
            type="button"
            onClick={() => navigate("/register")}
            className="text-pink-500 font-semibold hover:text-pink-600 hover:underline transition-colors"
          >
            Sign up
          </button>
        </div>
      </div>
    </div>
  );
};