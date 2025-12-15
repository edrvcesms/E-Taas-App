import { authApi } from "../axios/ApiServices";
import type { PasswordResetData } from "../../types/auth/ResetPassword";

export const forgotPassword = async (email: string) => {
  try {
    const response = await authApi.post("/forgot-password", null, {
      params: { email }
    });
    return response.data;
  } catch (error) {
    console.error("Forgot password request failed:", error);
    throw error;
  }
};

export const verifyPasswordResetOtp = async (email: string, otp: string) => {
  try {
    const response = await authApi.post("/verify-password-reset-otp", { email, otp });
    return response.data;
  } catch (error) {
    console.error("Password reset OTP verification failed:", error);
    throw error;
  }
};

export const resetPassword = async (data: PasswordResetData) => {
  try {
    const response = await authApi.post("/reset-password", data);
    return response.data;
  } catch (error) {
    console.error("Password reset failed:", error);
    throw error;
  } 
};