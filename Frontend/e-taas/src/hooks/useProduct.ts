import { useQuery } from "@tanstack/react-query";
import { getAllProducts } from "../services/products/Products";
import type { Product } from "../types/products/Product";
import { getProductById } from "../services/products/Products";
import type { ProductResponse } from "../types/products/Product";

export const useProduct = () => {
  const allProductsQuery = useQuery<Product[]>({
    queryKey: ["allProducts"],
    queryFn: getAllProducts,
    refetchOnWindowFocus: false,
  });

  return { allProductsQuery };
}

export const useProductDetails = (productId: number) => {
  const productDetailsQuery = useQuery<ProductResponse>({
    queryKey: ["productDetails", productId],
    queryFn: () => getProductById(productId),
    refetchOnWindowFocus: false,
    enabled: !!productId,
  });
  return { productDetailsQuery };
}
