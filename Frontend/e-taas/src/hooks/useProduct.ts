import { useQuery } from "@tanstack/react-query";
import { getAllProducts } from "../services/products/Products";
import type { Products } from "../types/products/Product";
import { getProductById } from "../services/products/Products";

export const useProduct = () => {
  const allProductsQuery = useQuery<Products[]>({
    queryKey: ["allProducts"],
    queryFn: getAllProducts,
    refetchOnWindowFocus: false,
  });

  return { allProductsQuery };
}

export const useProductDetails = (productId: number) => {
  const productDetailsQuery = useQuery<Products>({
    queryKey: ["productDetails", productId],
    queryFn: () => getProductById(productId),
    refetchOnWindowFocus: false,
    enabled: !!productId,
  });
  return { productDetailsQuery };
}
