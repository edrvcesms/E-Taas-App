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
      <div className="space-y-6">
        {data && data.length > 0 ? (
          data.map((product) => {


            return (
              <div
                key={product.id}
                className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md"
              >
                <h2 className="text-2xl font-bold mb-2 text-pink-600">{product.product_name}</h2>
                <p className="text-gray-700 mb-2">
                  Base Price: ${product.base_price.toFixed(2)}
                </p>
                {product.description && (
                  <p className="text-gray-600 mb-4">{product.description}</p>
                )}

                {product.variants && product.variants.length > 0 && (
                  <>
                    <h3 className="text-xl font-semibold mb-3 mt-6">Available Variants</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {product.variants.map((variant) => (
                        <div
                          key={variant.id}
                          className="border border-gray-200 p-4 rounded-lg hover:shadow-lg transition-shadow"
                        >
                          {variant.image_url ? (
                            <img
                              src={variant.image_url}
                              alt={variant.variant_name}
                              className="w-full h-40 object-cover rounded mb-3"
                            />
                          ) : (
                            <div className="h-40 bg-gray-200 flex items-center justify-center text-gray-500">
                              No image
                            </div>
                          )}
                          <h4 className="text-lg font-semibold mb-2">{variant.variant_name}</h4>
                          <p className="text-pink-600 font-bold mb-1">
                            {variant.price > 0 ? `$${variant.price.toFixed(2)}` : "Price unavailable"}
                          </p>
                          <p className="text-gray-600 text-sm">
                            Stock: {variant.stock > 0 ? variant.stock : "Out of stock"}
                          </p>
                          <button
                            className="w-full mt-3 bg-pink-500 text-white py-2 px-4 rounded hover:bg-pink-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                            disabled={variant.stock === 0}
                          >
                            {variant.stock > 0 ? "Add to Cart" : "Out of Stock"}
                          </button>
                        </div>
                      ))}
                    </div>
                  </>
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
