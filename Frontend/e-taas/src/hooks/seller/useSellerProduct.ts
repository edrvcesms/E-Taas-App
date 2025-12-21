import { getSellerProducts } from "../../services/seller/ShopProducts";
import { useQuery } from "@tanstack/react-query";
import type { Product } from "../../types/products/Product";
import { addProduct } from "../../services/products/ManageProducts";
import { useMutation } from "@tanstack/react-query";
import type { ProductData } from "../../types/products/ManageProduct";


export const useSellerProduct = () => {

  const sellerProductsQuery = useQuery<Product[]>({
    queryKey: ["sellerProducts"],
    queryFn: getSellerProducts,
    refetchOnWindowFocus: false,
  });

  const addNewProductMutation = useMutation({
    mutationFn: (productData: ProductData) => addProduct(productData),
    onSuccess: () => {
      sellerProductsQuery.refetch();
    },
    onError: (error) => {
      console.error("Adding new product failed:", error);
    },
  });



  return { sellerProductsQuery, addNewProductMutation };
}
