import { create } from 'zustand';
import type { Products } from '../types/products/Product';

interface ProductStore {
  products: Products[] | null;
  isLoading?: boolean;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  setProducts: (products: Products[]) => void;
}

export const useProductStore = create<ProductStore>((set) => ({
  products: null,
  isLoading: false,
  searchQuery: '',
  setSearchQuery: (query: string) => set({ searchQuery: query }),
  setProducts: (products: Products[]) => set({ products }),
}));