import { registerUser } from "../../../services/auth/RegisterService";
import type { RegisterData } from "../../../types/auth/Register";
import { useForm } from "../../../hooks/useForm";
import { useNavigate } from "react-router-dom";

interface FormData extends RegisterData {
  confirmPassword: string;
}

export const Register: React.FC = () => {

  const navigate = useNavigate();

  const { values, handleChange, reset } = useForm<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (values.password !== values.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
  
    const { username, email, password } = values;
    try {
      await registerUser({ username, email, password });
      sessionStorage.setItem("registerData", JSON.stringify({ username, email, password }));
      reset();
      navigate("/verify-otp");
    } catch (error) {
      alert("Registration failed. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold text-pink-500">Create Account</h1>
            <p className="text-gray-500">Join us today and get started</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Username</label>
              <input type="text" name="username" value={values.username} onChange={handleChange} required className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all" placeholder="Enter your username" />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" name="email" value={values.email} onChange={handleChange} required className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all" placeholder="Enter your email" />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" name="password" value={values.password} onChange={handleChange} required className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all" placeholder="Create a password" />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Confirm Password</label>
              <input type="password" name="confirmPassword" value={values.confirmPassword} onChange={handleChange} required className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all" placeholder="Confirm your password" />
            </div>

            <button type="submit" className="w-full bg-pink-500 text-white font-semibold py-3 rounded-lg hover:bg-pink-600 transform hover:scale-[1.02] transition-all shadow-lg shadow-pink-200">
              Register
            </button>
          </form>

          <div className="text-center">
            <p className="text-sm text-gray-600">
              Already have an account? <a href="#" className="text-pink-500 font-semibold hover:text-pink-600 transition-colors">Sign in</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}