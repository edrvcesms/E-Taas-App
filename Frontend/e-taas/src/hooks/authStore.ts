import { create } from "zustand"
import type { User } from "../types/user/User";
import { getUserDetails } from "../services/user/UserDetails";

type CurrentUserState = {
  currentUser: User | null;
  setCurrentUser: (user: User | null) => void;
  updateCurrentUser: (userData: Partial<User>) => void;
  clearCurrentUser: () => void;
  checkStoredUser: () => Promise<void>;
};

const STORAGE_KEY = "currentUser";

export const useCurrentUser = create<CurrentUserState>((set) => ({
  currentUser: null,

  setCurrentUser: (user) => {
    if (!user) {
      localStorage.removeItem(STORAGE_KEY);
      set({ currentUser: null });
      return;
    }

    localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
    set({ currentUser: user });
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
    set({ currentUser: null });
  },

  checkStoredUser: async () => {
    const storedUser = localStorage.getItem(STORAGE_KEY);

    if (storedUser) {
      try {
        set({ currentUser: JSON.parse(storedUser) });
        return;
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    }

    try {
      const userDetails = await getUserDetails();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userDetails));
      set({ currentUser: userDetails });
    } catch {
      set({ currentUser: null });
    }
  },
}));