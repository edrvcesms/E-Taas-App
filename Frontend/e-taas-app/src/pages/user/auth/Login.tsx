import React, { useEffect, useState } from "react";
import { Mail, Lock } from "lucide-react";
import type { LoginData } from "../../../types/Auth";
import { loginUser } from "../../../services/auth/UserAuth";
import { refreshUserToken } from "../../../services/auth/Token";
import authImage from "../../../components/auth/authImage";
import { useAuth } from "../../../context/AuthContext";
import { useUserSession } from "../../../hooks/userSession";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { getUserDetails } from "../../../services/user/UserDetails";

const Login = () => {
  useUserSession();

  const { isAuthenticated, setIsAuthenticated, isLoading, setIsLoading } = useAuth();
  const navigate = useNavigate();

  const { mutate } = useMutation({
    mutationFn: (formData: LoginData) => loginUser(formData),
    onSuccess: async (res) => {
      if (res.status === 200) {
        setIsAuthenticated(true);
        await getUserDetails();
        setIsLoading(false);
        navigate("/");
      }
    },
    onError: (error) => {
      console.log(error);
    },
    onSettled: () => {
      setIsLoading(false);
    },
  });

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated, navigate]);  

  const [formData, setFormData] = useState<LoginData>({
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    mutate(formData);
  };

  const handleGoogleSignIn = () => {
    alert("Google Sign In - Integration needed");
  };

  const handleFacebookSignIn = () => {
    alert("Facebook Sign In - Integration needed");
  };

  return (
    <>
      <div className="min-h-screen bg-gray-100 flex">
        {/* Left Column - Branding Section */}
        {authImage()}

        {/* Right Column - Form Section */}
        <div className="w-full lg:w-2/5 flex items-center justify-center p-8">
          <div className="w-full max-w-4xl">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="mb-8">
                <h2 className="text-3xl font-bold mb-2 text-gray-800">Welcome Back</h2>
                <p className="text-gray-600">Sign in to your account</p>
              </div>
              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Email Input */}
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="email"
                      name="email"
                      id="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="Enter your email"
                      required
                      className="w-full pl-12 pr-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-[#DD5BA3] focus:bg-white transition-all outline-none"
                    />
                  </div>
                </div>

                {/* Password Input */}
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="password"
                      name="password"
                      id="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter your password"
                      required
                      className="w-full pl-12 pr-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-[#DD5BA3] focus:bg-white transition-all outline-none"
                    />
                  </div>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-[#DD5BA3] hover:bg-[#C94A8F] text-white font-semibold py-3 rounded-xl transition-all duration-300 transform hover:scale-[1.01] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  {isLoading ? "Logging in..." : "Log In"}
                </button>

                {/* Divider */}
                <div className="relative my-6">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-white text-gray-500">OR</span>
                  </div>
                </div>

                {/* Social Sign In Buttons */}
                <button
                  type="button"
                  onClick={handleGoogleSignIn}
                  className="w-full flex items-center justify-center gap-3 bg-white border-2 border-gray-200 hover:border-gray-300 text-gray-700 font-medium py-3 rounded-xl transition-all duration-300"
                >
                  <svg className="w-5 h-5" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                  Sign in with Google
                </button>

                <button
                  type="button"
                  onClick={handleFacebookSignIn}
                  className="w-full flex items-center justify-center gap-3 bg-white border-2 border-gray-200 hover:border-gray-300 text-gray-700 font-medium py-3 rounded-xl transition-all duration-300"
                >
                  <svg className="w-5 h-5" fill="#1877F2" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                  Sign in with Facebook
                </button>

                {/* Sign Up Link */}
                <div className="text-center text-sm text-gray-600 mt-6">
                  Don't have an account?{" "}
                  <a onClick={() => navigate("/register")} className="text-[#DD5BA3] font-semibold hover:underline cursor-pointer">
                    Sign up
                  </a>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      {isAuthenticated && (
        <div className="fixed bottom-4 right-4">
          <button
            onClick={refreshUserToken}
            className="bg-[#DD5BA3] hover:bg-[#C94A8F] text-white py-2 px-4 rounded-lg transition-colors shadow-lg"
          >
            Refresh Token
          </button>
        </div>
      )}
    </>
  );
};

export default Login;