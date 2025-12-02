import { authApi } from "../axios";
import type { EmailVerificationData } from "../../types/auth/EmailVerification";

export const verifyEmail = async (data: EmailVerificationData) => {
  try {
    const response = await authApi.post("/verify-email-otp", data);
    return response.data;
  } catch (error) {
    console.error("Email verification failed:", error);
    throw error;
  }
};
