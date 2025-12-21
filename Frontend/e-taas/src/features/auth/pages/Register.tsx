import { RegisterForm } from "../components/RegisterForm";

export const Register: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-pink-50 to-gray-100 p-4 py-8">
      <RegisterForm />
    </div>
  );
};