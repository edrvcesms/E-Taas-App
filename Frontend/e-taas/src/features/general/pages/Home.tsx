import { loginUser } from "../../../services/auth/LoginService";
import { notificationWebSocket } from "../../../services/websocket/Clients";
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

    const setupWebSocket = async () => {
      try {
        const socket = notificationWebSocket();
        console.log("Connecting to WebSocket...");
        socket.onopen = () => {
          console.log("WebSocket connected.");
        };
      } catch (error) {
        console.error("WebSocket connection error:", error);
      }
    };

    setupWebSocket();
  }, []);

  return (
    <>
      <div className="text-3xl">Welcome to E-Taas Home Page</div>
    </>
  );
}