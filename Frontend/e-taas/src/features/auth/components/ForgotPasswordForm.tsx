import { useForm } from "../../../hooks/useForm";
import { useNavigate } from "react-router-dom";
import { forgotPassword } from "../../../services/auth/ResetPassword";

export const ForgotPasswordForm: React.FC = () => {

  const navigate = useNavigate();

  const { values, handleChange, reset } = useForm<{ email: string }>({
    email: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await forgotPassword(values.email);
      sessionStorage.setItem("resetEmail", values.email);
      reset();
      navigate("/reset-password-verify-otp");
    } catch (error) {
      console.error(error);
      alert("Failed to initiate password reset. Please try again.");
    }
  };

  return (
    <>
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
        <button
          type="submit"
          className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold"
        >
          Send OTP
        </button>
      </form>
    </>
  );
}