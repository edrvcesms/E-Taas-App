import { LoadingIndicator } from "../components/LoadingIndicator";
import { MapPin, Star } from "lucide-react"
import { useProductStore } from "../../../store/useProductStore";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useProduct } from "../../../hooks/useProduct";

export const ProductsPage: React.FC = () => {
  const products = useProductStore((state) => state.products);
  const isLoading = useProductStore((state) => state.isLoading);

  const { allProductsQuery } = useProduct();
  const setProduct = useProductStore((state) => state.setProducts);

  useEffect(() => {
    if (allProductsQuery.data) {
      setProduct(allProductsQuery.data);
    }
  }, [allProductsQuery.data, setProduct]);
  

  const navigate = useNavigate();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingIndicator size={60} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-500/5 to-white p-4">
      <h1 className="text-4xl font-bold text-center mb-8 text-pink-500">Our Products</h1>
      <div className="max-w-7xl mx-auto flex flex-wrap gap-10 justify-start " >
        {products && products.length > 0 ? (
          products.map((product) => {
            return (
              <div
                onClick={() => navigate(`/products/${product.id}`)}
                key={product.id}
                className="w-2xs p-4 bg-white rounded-2xl shadow-md cursor-pointer hover:shadow-xl transition-shadow duration-300"
              >
                {product.images && product.images.length > 0 && (
                  <img
                    src={product.images[0].image_url}
                    alt={`${product.product_name} image`}
                    className="
                      w-full
                      h-40
                      object-cover
                      rounded-xl
                      mb-4
                      border
                      border-gray-200
                    "
                  />
                )}

                {product.category && (
                  <div className="flex items-center mb-1">
                    <span className="text-gray-400 text-sm font-medium">{product.category.category_name}</span>
                  </div>
                )}

                <h2 className="text-lg font-semibold mb-1 text-gray-700 line-clamp-2">{product.product_name}</h2>

                <p className="text-pink-500 mb-2 font-bold text-xl">
                  ₱{product.base_price.toFixed(2)}
                </p>

                {product.seller && (
                  <div className="flex items-center mb-2">
                    <Star className="w-4 h-4 text-yellow-400 mr-1" />
                    <span className="text-gray-700 text-sm font-medium">{product.seller.ratings}</span>
                  </div>
                )}
                <hr className="my-3 border-t border-gray-200" />
                {product.seller && (
                  <div className="flex items-center text-gray-600 text-sm">
                    <MapPin className="w-4 h-4 text-pink-500 mr-1 shrink-0" />
                    <span className="line-clamp-1">{product.seller.business_address}</span>
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
