import { resetPassword } from "../../../services/auth/ResetPassword";
import { useForm } from "../../../hooks/general/useForm";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import type { PasswordResetData } from "../../../types/auth/ResetPassword";

interface FormData extends PasswordResetData {
  confirm_password: string;
}

export const ResetPasswordForm: React.FC = () => {

  const navigate = useNavigate();
  const { values, handleChange, reset } = useForm<FormData>({
    email: "",
    new_password: "",
    confirm_password: "",
  });

  const stored_email = sessionStorage.getItem('verifiedResetEmail');

  useEffect(() => {
    if (!stored_email) {
      navigate('/reset-password-verify-otp');
    }
  }, [navigate, stored_email]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (stored_email) {
      values.email = stored_email;
    }

    if (values.new_password !== values.confirm_password) {
      alert("Passwords do not match");
      return;
    };

    const { email, new_password } = values;

    try {
      await resetPassword({ email, new_password });
      alert("Password reset successful! Please log in with your new password.");
      sessionStorage.removeItem("resetEmail");
      reset();
      navigate("/login");
    } catch (error) {
      alert("Password reset failed. Please try again.");
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">New Password</label>
        <input
          type="password"
          name="new_password"
          value={values.new_password}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
          placeholder="Enter your new password"
        />
      </div>
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Confirm Password</label>
        <input
          type="password"
          name="confirm_password"
          value={values.confirm_password}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
          placeholder="Confirm your new password"
        />
      </div>
      <button
        type="submit"
        className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold"
      >
        Reset Password
      </button>
    </form>
  );
}

