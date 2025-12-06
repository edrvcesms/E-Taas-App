
export interface VariantData {
  stock: number; 
  price: number;
}

interface VariantAttribute {
  value: string;
}

interface VariantCategoryData{
  category_name: string;
  attributes: VariantAttribute[];
}

interface UpdateCategoryData {
  id: number;
  category_name: string;
  attributes: {
    id: number;
    value: string;
  }[];
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
  variant_categories?: VariantCategoryData[];
  variants?: VariantData[] | [{}];
}

export interface UpdateProductData {
  product: ProductData;
  variant_categories?: UpdateCategoryData[]
}

