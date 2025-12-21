import React, { useState } from "react";
import { registerUser } from "../../../services/auth/RegisterService";
import type { RegisterData } from "../../../types/auth/Register";
import { User, Mail, Lock, Eye, EyeOff } from "lucide-react";
import { useForm } from "../../../hooks/useForm";
import { useNavigate } from "react-router-dom";
import { useCurrentUser } from "../../../store/currentUserStore";
import { useMyContext } from "../../../context/MyContext";

interface FormData extends RegisterData {
  confirmPassword: string;
}

export const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const { isLoading, setIsLoading } = useMyContext(); 
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const { values, handleChange, reset } = useForm<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    if (values.password !== values.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const { username, email, password } = values;
    try {
      await registerUser({ username, email, password });
      sessionStorage.setItem("registerData", JSON.stringify({ username, email, password }));
      reset();
      navigate("/verify-register-otp");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col p-8 bg-white border border-gray-200 rounded-xl shadow-lg w-full max-w-xl transition-all duration-300 hover:shadow-xl">
      {/* Logo - Uncomment and add your logo if needed */}
      {/* <div className="flex justify-center mb-6">
        <img src={logo} alt="Logo" className="h-28 w-28 object-contain" />
      </div> */}

      <h2 className="text-3xl font-bold text-start text-pink-500 mb-2">
        Create Account
      </h2>

      <p className="text-start text-gray-500 mb-6">
        Join us today and get started
      </p>

      <form className="flex flex-col space-y-5" onSubmit={handleSubmit}>
        {/* Username Input */}
        <div className="relative">
          <label htmlFor="username" className="font-medium text-gray-700 mb-1 block">
            Username
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              name="username"
              id="username"
              value={values.username}
              onChange={handleChange}
              className="border border-gray-300 text-gray-800 pl-10 rounded-lg p-3 w-full bg-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500 transition duration-300 outline-none"
              autoComplete="username"
              placeholder="Enter your username"
              required
            />
          </div>
        </div>

        {/* Email Input */}
        <div className="relative">
          <label htmlFor="email" className="font-medium text-gray-700 mb-1 block">
            Email Address
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="email"
              name="email"
              id="email"
              value={values.email}
              onChange={handleChange}
              className="border border-gray-300 text-gray-800 pl-10 rounded-lg p-3 w-full bg-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500 transition duration-300 outline-none"
              autoComplete="email"
              placeholder="your.email@example.com"
              required
            />
          </div>
        </div>

        {/* Password Input */}
        <div className="relative">
          <label htmlFor="password" className="font-medium text-gray-700 mb-1 block">
            Password
          </label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              id="password"
              value={values.password}
              onChange={handleChange}
              className="border border-gray-300 text-gray-800 pl-10 pr-10 rounded-lg p-3 w-full bg-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500 transition duration-300 outline-none"
              placeholder="••••••••"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Confirm Password Input */}
        <div className="relative">
          <label htmlFor="confirmPassword" className="font-medium text-gray-700 mb-1 block">
            Confirm Password
          </label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              name="confirmPassword"
              id="confirmPassword"
              value={values.confirmPassword}
              onChange={handleChange}
              className="border border-gray-300 text-gray-800 pl-10 pr-10 rounded-lg p-3 w-full bg-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500 transition duration-300 outline-none"
              placeholder="••••••••"
              required
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
            >
              {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full cursor-pointer flex items-center justify-center gap-2 bg-pink-600 text-white py-3 rounded-lg font-medium hover:bg-pink-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <svg aria-hidden="true" className="w-5 h-5 mr-2 text-white animate-spin fill-pink-300" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor" />
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill" />
              </svg>
              Signing up...
            </>
          ) : (
            "Sign Up"
          )}
        </button>

        <div className="flex items-center justify-center">
          <p className="text-center text-gray-500 mr-1">Already have an account?</p>
          <button
            type="button"
            onClick={() => navigate("/login")}
            className="text-center text-pink-600 font-medium hover:text-pink-800 hover:underline transition-colors"
          >
            Sign in
          </button>
        </div>
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
    </div>
  );
};