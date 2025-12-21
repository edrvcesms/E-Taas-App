import { RegisterForm } from "../components/RegisterForm";

export const Register: React.FC = () => {

  return (
      <div className="min-h-screen flex items-start justify-center bg-gray-50 md:p-12 p-4 pt-12">
        <RegisterForm />
      </div>
  );
}