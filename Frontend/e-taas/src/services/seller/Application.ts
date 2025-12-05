import type { SellerApplicationData } from "../../types/seller/Application";
import { sellerApi } from "../axios/ApiServices";


export const submitSellerApplication = async (data: SellerApplicationData) => {
  try {
    const res = await sellerApi.post("/apply", data);
    return res.data;
  } catch (error) {
    console.error("Submitting seller application failed:", error);
    throw error;
  }
};