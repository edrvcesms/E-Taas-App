import { authApi } from "../axios/ApiServices";
import type { LoginData } from "../../types/auth/Login";

export const loginUser = async (data: LoginData) => {
  try {
    const response = await authApi.post("/login", data, {withCredentials: true});
    console.log("Login response data:", response.data);
    return response.data.user;
  } catch (error) {
    throw error;
  }
};