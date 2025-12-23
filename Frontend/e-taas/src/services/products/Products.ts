import { productApi } from "../axios/ApiServices";


export const getAllProducts = async () => {
  try {
    const res = await productApi.get("/");
    return res.data;
  } catch (error) {
    console.error("Fetching products failed:", error);
    throw error;
  }
}


export const getProductById = async (productId: number) => {
  try {
    const res = await productApi.get(`/${productId}`);
    return res.data;
  } catch (error) {
    console.error("Fetching product by ID failed:", error);
    throw error;
  }
}

export const getAllProductCategories = async () => {
  try {
    const res = await productApi.get("/categories/all");
    return res.data;
  } catch (error) {
    console.error("Fetching product categories failed:", error);
    throw error;
  }
}