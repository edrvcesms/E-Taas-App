import { authApi } from "../axios";
import type { RegisterData } from "../../types/auth/Register";

export const registerUser = async (data: RegisterData) => {
  try{
    const response = await authApi.post("/register", data);
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};