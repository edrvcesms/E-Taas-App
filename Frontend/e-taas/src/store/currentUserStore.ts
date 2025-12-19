import { create } from "zustand"
import type { User } from "../types/user/User";
import { getUserDetails } from "../services/user/UserDetails";

type CurrentUserState = {
  currentUser: User | null;
  isLoading?: boolean;
  isLoggedIn?: boolean;
  setCurrentUser: (user: User | null) => void;
  updateCurrentUser: (userData: Partial<User>) => void;
  clearCurrentUser: () => void;
  checkStoredUser: () => Promise<void>;
};

const STORAGE_KEY = "currentUser";

export const useCurrentUser = create<CurrentUserState>((set) => ({
  currentUser: null,

  isLoading: true,
  isLoggedIn: false,

  setCurrentUser: (user) => {
    if (!user) {
      localStorage.removeItem(STORAGE_KEY);
      set({ currentUser: null, isLoading: false });
      return;
    }

    localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
    set({ currentUser: user, isLoading: false, isLoggedIn: true });
  },

  updateCurrentUser: (userData) => {
    set((state) => {
      if (!state.currentUser) return state;

      const updatedUser = { ...state.currentUser, ...userData };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedUser));

      return { currentUser: updatedUser };
    });
  },

  clearCurrentUser: () => {

    localStorage.removeItem(STORAGE_KEY);
    set({ currentUser: null, isLoading: false, isLoggedIn: false });
  },

  checkStoredUser: async () => {
    set({ isLoading: true });

    try {
      const storedUser = localStorage.getItem(STORAGE_KEY);

      if (storedUser) {
        const parsedUser = JSON.parse(storedUser);
        set({ currentUser: parsedUser, isLoading: false, isLoggedIn: true });
        return;
      }

      const userDetails = await getUserDetails();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userDetails));
      set({ currentUser: userDetails, isLoading: false, isLoggedIn: true });

    } catch (error) {
      console.error('Error checking stored user:', error);
      localStorage.removeItem(STORAGE_KEY);
      set({ currentUser: null, isLoading: false, isLoggedIn: false });
    }
  },
}));