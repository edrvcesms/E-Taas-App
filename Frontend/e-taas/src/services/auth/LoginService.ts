import { authApi } from "../axios";
import type { LoginData } from "../../types/auth/Login";

export const loginUser = async (data: LoginData) => {
  try {
    const response = await authApi.post("/login", data);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
};