import { sellerApi } from "../axios/ApiServices";

export const getShopDetails = async () => {
  try {
    const res = await sellerApi.get("/shop-details");
    return res.data;
  } catch (error) {
    console.error("Fetching shop details failed:", error);
    throw error;
  }
}