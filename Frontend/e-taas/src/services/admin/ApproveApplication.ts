import { adminApi } from "../axios/ApiServices";

export const approveSellerApplication = async (sellerId: number) => {
  try {
    const res = await adminApi.post("/verify-seller", { sellerId });
    return res.data;
  } catch (error) {
    console.error("Approving seller application failed:", error);
    throw error;
  }
};