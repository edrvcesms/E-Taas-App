
import Footer from "../../../layouts/Footer";
import { LoadingIndicator } from "../components/LoadingIndicator";
import { useParams } from "react-router-dom";

export const ProductDetails: React.FC = () => {
  const { productId } = useParams<{ productId: string }>();
  const { data, isLoading, isError } = useProduct(Number(productId))

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingIndicator size={60} />
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <p className="text-red-600 text-xl mb-2">Error loading product details</p>
          <p className="text-gray-600">Please try refreshing the page</p>
        </div>
      </div>
    );
  }

  console.log("productId:", productId)
  console.log("data:", data)
  console.log("isLoading:", isLoading)
  console.log("isError:", isError)

  return (
    <>
      {data && (
        <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 p-6">
          <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6">
            <h1 className="text-4xl font-bold text-pink-500 mb-4">{data.product.product_name}</h1>
          </div>
          <Footer />
        </div>
      )}
    </>
  );
}