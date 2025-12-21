import { VerifyEmailForm } from "../components/VerifyEmailForm";


export const VerifyRegisterOtp: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-pink-50 to-gray-100 p-4 py-8">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-2xl p-8 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-pink-500">Verify Your Email</h1>
          <p className="text-gray-500">Enter the OTP sent to your email to complete your registration</p>
        </div>
        <VerifyEmailForm />
      </div>
    </div>
  );
};