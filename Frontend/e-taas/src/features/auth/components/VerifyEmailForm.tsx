import type { EmailVerificationData } from "../../../types/auth/EmailVerification";
import { verifyEmail } from "../../../services/auth/EmailVerificationService";
import { useForm } from "../../../hooks/useForm";
import type React from "react";

export const VerifyEmailForm: React.FC = () => {
  const { values, handleChange, reset } = useForm<EmailVerificationData>({
    username: "",
    email: "",
    password: "",
    otp: "",
  });

  const storedData = sessionStorage.getItem("registerData");
  if (storedData) {
    const { username, email, password } = JSON.parse(storedData);
    values.username = username;
    values.email = email;
    values.password = password;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await verifyEmail(values);
      alert("Email verification successful!");
      sessionStorage.removeItem("registerData");
      reset();
    } catch (error) {
      alert("Email verification failed. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">OTP</label>
          <input
            type="text"
            name="otp"
            value={values.otp}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
            placeholder="Enter the OTP"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition-all font-semibold"
        >
          Verify Otp
        </button>
      </form>
  );
};