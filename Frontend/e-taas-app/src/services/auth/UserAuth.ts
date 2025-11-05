import { authApi } from "../axios"
import type { LoginData } from "../../types/Auth"
import type { RegisterData } from "../../types/Auth";


export const registerUser = async (registerData: RegisterData) => {
  try {
    const res = await authApi.post("/register", registerData);
    return res;
  }catch(e){
    console.log(e);
    throw new Error("Failed to register user.")
  }
}

export const loginUser = async (credentials: LoginData) => {
  try {
    const response = await authApi.post("/login", credentials, { withCredentials: true });
    return response;
  }catch(e){
    console.log(e);
    throw new Error("Failed to login user.")
  }
}

