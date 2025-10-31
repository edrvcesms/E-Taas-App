import { authApi } from "../axios"
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