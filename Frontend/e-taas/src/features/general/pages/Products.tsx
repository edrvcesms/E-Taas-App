import { getAllProducts } from "../../../services/products/Products";
import { useQuery } from "@tanstack/react-query";
import { LoadingIndicator } from "../components/LoadingIndicator";
import { MapPin, Star } from "lucide-react"
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
    <div className="min-h-screen bg-linear-to-br from-pink-500/5 to-white p-8">
      <h1 className="text-4xl font-bold text-center mb-8 text-pink-500">Our Products</h1>
      <div className="flex flex-wrap gap-8 justify-start">
        {data && data.length > 0 ? (
          data.map((product) => {
            return (
              <div
                key={product.id}
                className="min-w-[24rem] p-6 bg-white rounded-3xl shadow-md"
              >
                {product.images && product.images.length > 0 && (
                  <img
                    src={product.images[0].image_url}
                    style={{ objectFit: "contain" }}
                    alt={`${product.product_name} Image 1`}
                    className="w-96 h-60 object-contain rounded-3xl mb-6 border border-gray-200"
                  />
                )}

                {product.category && (
                  <div className="flex items-center mb-2">
                    <span className="text-gray-400 font-medium">{product.category.category_name}</span>
                  </div>
                )}

                <h2 className="text-2xl font-semibold mb-2 text-gray-700">{product.product_name}</h2>

                <p className="text-pink-500 mb-3 font-bold text-2xl">
                  ₱{product.base_price.toFixed(2)}
                </p>
                
                {product.seller && (
                  <div className="flex items-center mb-2">
                    <Star className="w-5 h-5 text-yellow-400 mr-2" />
                    <span className="text-gray-700 font-medium">{product.seller.ratings}</span>
                  </div>
                )}
                <hr className="my-4 border-t border-gray-200" />
                {product.seller && (
                  <div className="flex items-center text-gray-600">
                    <MapPin className="w-5 h-5 text-pink-500 mr-2" />
                    <span>{product.seller.business_address}</span>
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
