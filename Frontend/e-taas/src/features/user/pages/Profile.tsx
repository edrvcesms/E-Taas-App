import { useCurrentUser } from "../../../store/currentUserStore";
import { Profile } from "./UserProfile";
import { SellerProfile } from "../../seller/pages/SellerProfile";

export const ProfilePage = () => {
  const currentUser = useCurrentUser((state) => state.currentUser);
  return (
    <>
      {currentUser?.seller?.is_seller_mode ? <SellerProfile /> : <Profile />}
    </>
  );
};