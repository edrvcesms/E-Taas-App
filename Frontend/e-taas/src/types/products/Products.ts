
interface VariantData {
  stock: number; 
  price: number;
}


interface VariantAttribute {
  value: string;
}

interface VariantCategory{
  category_name: string;
  attributes: VariantAttribute[];
}

interface Product {
  product_name: string;
  description: string;
  base_price: number;
  stock: number;
  has_variants: boolean;
  category_id: number;
}

export interface ProductData {
  product: Product;
  variant_categories?: VariantCategory[];
  variants?: VariantData[];
}