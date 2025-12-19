import { productApi } from "../axios/ApiServices";
import type { ProductData, UpdateProductData, VariantData } from "../../types/products/ManageProduct";

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


export const addVariantImage = async (image: FormData, variantId: number) => {
  try {
    const res = await productApi.post(`/add-variant-image/${variantId}`,image);
    return res.data;
  } catch (error) {
    console.error("Adding variant image failed:", error);
    throw error;
  }
};


export const updateProduct = async (productId: number, data: UpdateProductData) => {
  try {
    const res = await productApi.put(`/update-product/${productId}`, data);
    return res.data;
  } catch (error) {
    console.error("Updating product failed:", error);
    throw error;
  }
};

export const updateProductVariant = async (variantId: number, data: VariantData) => {
  try {
    const res = await productApi.put(`/update-variant/${variantId}`, data);
    return res.data;
  } catch (error) {
    console.error("Updating product variant failed:", error);
    throw error;
  }
};

export const deleteProduct = async (productId: number) => {
  try {
    const res = await productApi.delete(`/delete-product/${productId}`);
    return res.data;
  } catch (error) {
    console.error("Deleting product failed:", error);
    throw error;
  }
};