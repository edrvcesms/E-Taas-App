import type { SellerDetails } from "../seller/Seller";

export interface ProductResponse {
  product: Product;
}

export interface Product {
  id: number;
  product_name: string;
  description?: string;
  base_price: number;
  stock: number;
  has_variants: boolean;
  category_id: number;
  seller_id: number;
  created_at: string;

  category: ProductCategory;
  images: ProductImage[];
  seller: SellerDetails;
  variants: VariantDetails[];
}

export interface ProductImage {
  id: number;
  image_url: string;
  product_id: number;
}

export interface VariantDetails {
  id: number;
  stock: number;
  price: number;
  variant_name: string;
  image_url?: string;
}

export interface ProductCategory {
  id: number;
  category_name: string;
}
