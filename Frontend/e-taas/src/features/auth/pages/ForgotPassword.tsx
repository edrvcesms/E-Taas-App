import { ForgotPasswordForm } from "../components/ForgotPasswordForm";

export const ForgotPassword: React.FC = () => {

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold text-pink-500">Forgot Password</h1>
            <p className="text-gray-500">Enter your email to reset your password</p>
          </div>
          <ForgotPasswordForm />
        </div>
      </div>
    </div>
  );
}