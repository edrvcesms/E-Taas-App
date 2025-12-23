import { useQuery } from "@tanstack/react-query";
import { getAllProductCategories } from "../../services/products/Products";
import type { ProductCategory } from "../../types/products/Product";

export const useProductCategories = () => {
  const productCategoriesQuery = useQuery<ProductCategory[]>({
    queryKey: ["productCategories"],
    queryFn: getAllProductCategories,
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
  });
  return { productCategoriesQuery };
}