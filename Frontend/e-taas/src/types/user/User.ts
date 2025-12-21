import type { SellerDetails } from "../seller/Seller";


export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  middle_name?: string;
  last_name?: string;
  address?: string;
  contact_number?: string;
  is_seller: boolean;
  is_admin: boolean;
  seller?: SellerDetails;
}

export interface UpdateUserData {
  first_name?: string;
  middle_name?: string;
  last_name?: string;
  birthdate?: string;
  address?: string;
  contact_number?: string;
}