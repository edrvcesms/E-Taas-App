import { switchUserRole } from "../../services/user/SwitchRole";
import { useCurrentUser } from "../../store/currentUserStore";
import { useState } from "react";

export const useSwitchRole = () => {
  const currentUser = useCurrentUser((state) => state.currentUser);
  const [isSellerMode, setIsSellerMode] = useState(currentUser?.seller?.is_seller_mode || false);
  const updateCurrentUser = useCurrentUser((state) => state.updateCurrentUser);

  const toggleRole = async () => {
    try {
      await switchUserRole(!isSellerMode);
      setIsSellerMode(!isSellerMode);
      updateCurrentUser({ seller: { is_seller_mode: !isSellerMode } });
    } catch (error) {
      console.error("Error switching user role:", error);
    }
  };

  return { isSellerMode, toggleRole };
}