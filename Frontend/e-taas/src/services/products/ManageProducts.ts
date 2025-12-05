import { productApi } from "../axios/ApiServices";
import type { ProductData } from "../../types/products/Products";

export const addProduct = async (data: ProductData) => {
  try {
    const res = await productApi.post("/add-product", data);
    return res.data;
  } catch (error) {
    console.error("Adding product failed:", error);
    throw error;
  }
};

export const addImageToProduct = async (images: FormData, productId: number) => {
  try {
    const res = await productApi.post(`/add-images/${productId}`,images);
    return res.data;
  } catch (error) {
    console.error("Adding images failed:", error);
    throw error;
  }
};
