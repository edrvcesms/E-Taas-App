import { create } from "zustand"
import type { User } from "../types/user/User";

type CurrentUserState = {
  currentUser: User | null;
  setCurrentUser: (user: User | null) => void;
  updateCurrentUser: (userData: Partial<User>) => void;
  clearCurrentUser: () => void;
}

export const useCurrentUser = create<CurrentUserState>((set) => {
  return {
    currentUser: null,
    setCurrentUser: (user: User | null) => set({ currentUser: user }),
    updateCurrentUser: (userData: Partial<User>) => set((state) => ({
      currentUser: state.currentUser ? { ...state.currentUser, ...userData } : null
    })),
    clearCurrentUser: () => set({ currentUser: null }),
  }
})