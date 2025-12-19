export interface ProductDetails {
  id: number;
  product_name: string;
  description?: string;
  base_price: number;
  stock: number;
  has_variants: boolean;
  category_id: number;
  seller_id: number;
  variants?: VariantDetails[];
}

export interface VariantDetails {
  id: number;
  stock: number;
  price: number;
  image_url?: string;
  variant_name: string;
}
