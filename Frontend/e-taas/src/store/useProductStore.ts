import { create } from 'zustand';
import type { Product } from '../types/products/Product';

interface ProductStore {
  products: Product[] | null;
  isLoading?: boolean;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  setProducts: (products: Product[]) => void;
}

export const useProductStore = create<ProductStore>((set) => ({
  products: null,
  isLoading: false,
  searchQuery: '',
  setSearchQuery: (query: string) => set({ searchQuery: query }),
  setProducts: (products: Product[]) => set({ products }),
}));