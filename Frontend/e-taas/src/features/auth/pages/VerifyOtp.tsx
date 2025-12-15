import type { EmailVerificationData } from "../../../types/auth/EmailVerification";
import { verifyEmail } from "../../../services/auth/EmailVerificationService";
import { useForm } from "../../../hooks/useForm";
import type React from "react";

export const VerifyOtp: React.FC = () => {
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
    <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold text-pink-500">Verify Your Email</h1>
            <p className="text-gray-500">Enter the OTP sent to your email</p>
          </div>
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
              Verify Email
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};