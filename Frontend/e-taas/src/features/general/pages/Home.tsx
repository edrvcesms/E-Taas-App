import { loginUser } from "../../../services/auth/LoginService";
import { useEffect } from "react";

export const Home: React.FC = () => {

  const email : string = "user2@example.com";
  const password: string = "string";

  useEffect(() => {
    const performLogin = async () => {
      try {
        const response = await loginUser({ email, password });
        console.log("Login successful:", response);
      } catch (error) {
        console.error("Login error:", error);
      }
    };

    performLogin();
  }, []);

  return (
    <>
      <div className="text-3xl">Welcome to E-Taas Home Page</div>
    </>
  );
}