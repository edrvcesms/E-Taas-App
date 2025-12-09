import { authApi } from "../axios/ApiServices";

export const refreshToken = async () => {
  try {
    const res = await authApi.post("/token/refresh", {}, {withCredentials: true});
    return res.data;
  } catch (error) {
    console.error("Token refresh failed:", error);
    throw error;
  }
};