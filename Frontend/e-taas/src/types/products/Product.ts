import type { SellerDetails } from "../seller/Seller";

export interface ProductDetails {
  id: number;
  product_name: string;
  description?: string;
  base_price: number;
  stock: number;
  has_variants: boolean;
  category_id: number;
  seller_id: number;
  images: ProductImage[];
  variants?: VariantDetails[];
  seller: SellerDetails;
  category: ProductCategory;
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
  image_url?: string;
  variant_name: string;
}

export interface ProductCategory {
  id: number;
  category_name: string;
}
