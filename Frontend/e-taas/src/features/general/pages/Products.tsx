import { useCurrentUser } from "../../../store/currentUserStore";
import { AllProducts } from "../components/AllProducts";
import ManageProductPage from "../../seller/pages/ManageProduct";

export const ProductsPage: React.FC = () => {
  const { currentUser } = useCurrentUser();

  return (
    <>
      {currentUser?.seller?.is_seller_mode ? (
        <ManageProductPage />
      ) : (
        <AllProducts />
      )}
    </>
  )

};
