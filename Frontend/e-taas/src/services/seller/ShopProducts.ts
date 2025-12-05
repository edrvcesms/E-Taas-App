import { sellerApi } from "../axios/ApiServices";

export const getSellerProducts = async () => {
  try {
    const res = await sellerApi.get("/my-products");
    return res.data;
  } catch (error) {
    console.error("Fetching seller products failed:", error);
    throw error;
  }
}