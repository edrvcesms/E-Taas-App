import { RegisterForm } from "../components/RegisterForm";

export const Register: React.FC = () => {

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <RegisterForm />
      </div>
    </div>
  );
}