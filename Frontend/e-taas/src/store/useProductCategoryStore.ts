import { create } from "zustand";
import type { ProductCategory } from "../types/products/Product";

interface ProductCategoryStore {
  categories: ProductCategory[] | null;
  isLoading?: boolean;
  setCategories: (categories: ProductCategory[]) => void;
}

export const useProductCategoryStore = create<ProductCategoryStore>((set) => ({
  categories: null,
  isLoading: false,
  setCategories: (categories: ProductCategory[]) => set({ categories }),
}));

