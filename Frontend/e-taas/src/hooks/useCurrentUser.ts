import { create } from "zustand"
import type { User } from "../types/user/User";
import useLocalStorage from "./useLocalStorage";

type CurrentUserState = {
  currentUser: User | null;
  setCurrentUser: (user: User | null) => void;
  updateCurrentUser: (userData: Partial<User>) => void;
  clearCurrentUser: () => void;
}


export const useCurrentUser = create<CurrentUserState>((set) => {

  const [storedUser, setStoredUser] = useLocalStorage<User | null>("currentUser", null);

  const currentUser = storedUser;

  return {
    currentUser,
    setCurrentUser: (user: User | null) => {
      setStoredUser(user);
      set({ currentUser: user });
    },
    updateCurrentUser: (userData: Partial<User>) => set((state) => ({
      currentUser: state.currentUser ? { ...state.currentUser, ...userData } : null
    })),
    clearCurrentUser: () => {
      setStoredUser(null);
      set({ currentUser: null });
    },
  }
});
