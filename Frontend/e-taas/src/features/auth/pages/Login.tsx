import { loginUser } from "../../../services/auth/LoginService";
import type { LoginData } from "../../../types/auth/Login";
import { useForm } from "../../../hooks/useForm";
import { useCurrentUser } from "../../../hooks/useCurrentUser";

export const Login: React.FC = () => {
  const { values, handleChange, reset } = useForm<LoginData>({
    email: "",
    password: "",
  });

  const { setCurrentUser } = useCurrentUser();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const user = await loginUser(values);
      setCurrentUser(user);
      reset();
    } catch (error) {
      alert("Login failed. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold text-pink-500">Welcome Back</h1>
            <p className="text-gray-500">Log in to your account</p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" name="email" value={values.email} onChange={handleChange} required className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all" placeholder="Enter your email" />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" name="password" value={values.password} onChange={handleChange} required className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all" placeholder="Enter your password" />
            </div>
            <button type="submit" className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold">
              Log In
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
