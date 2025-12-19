import { getAllProducts } from "../../../services/products/Products";
import { useQuery } from "@tanstack/react-query";
import { LoadingIndicator } from "../components/LoadingIndicator";
import type { ProductDetails } from "../../../types/products/Product";

export const ProductsPage: React.FC = () => {
  const { data, isLoading, isError } = useQuery<ProductDetails[]>({
    queryKey: ["products"],
    queryFn: getAllProducts,
  });

  console.log("Fetched Products Data:", data);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingIndicator size={60} />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <p className="text-red-600 text-xl mb-2">Error loading products</p>
          <p className="text-gray-600">Please try refreshing the page</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-4xl font-bold text-center mb-8 text-pink-500">Our Products</h1>
      <div className="flex flex-wrap gap-8 justify-start">
        {data && data.length > 0 ? (
          data.map((product) => {
            return (
              <div
                key={product.id}
                className="min-w-md p-6 bg-white rounded-lg shadow-md"
              >
                {product.images && product.images.length > 0 && (
                  <img
                    src={product.images[0].image_url}
                    alt={`${product.product_name} Image 1`}
                    className="w-full h-50 object-cover rounded mb-6"
                  />
                )}
                <h2 className="text-2xl font-semibold mb-2 text-gray-700">{product.product_name}</h2>
                <p className="text-pink-500 mb-3 font-bold text-2xl">
                  ₱{product.base_price.toFixed(2)}
                </p>
                {product.description && (
                  <p className="text-gray-600 mb-4">{product.description}</p>
                )}

                {product.seller.ratings && (
                  <div className="flex items-center mb-4">
                    <span className="text-yellow-500 mr-2">★</span>
                    <span className="text-gray-700 font-semibold">{product.seller.ratings.toFixed(1)}</span>
                  </div>
                )}
                
              </div>
            );
          })
        ) : (
          <div className="flex justify-center items-center h-64">
            <p className="text-gray-600 text-xl">No products available.</p>
          </div>
        )}
      </div>
    </div>
  );
};
