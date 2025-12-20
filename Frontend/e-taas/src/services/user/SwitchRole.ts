import { sellerApi } from "../axios/ApiServices";

export const switchUserRole = async (isSellerMode: boolean) => {
  try {
    const res = await sellerApi.put("/switch-role", { is_seller_mode: isSellerMode });
    return res.data;
  } catch (error) {
    console.error("Switching user role failed:", error);
    throw error;
  }
}