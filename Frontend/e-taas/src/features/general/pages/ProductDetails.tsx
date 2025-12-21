import { useState } from 'react';
import { ArrowLeft, Check, Share2, Heart, ShoppingCart, Store, Shield, Truck, Package, ChevronLeft, ChevronRight, CreditCard } from 'lucide-react';
import { useParams, useNavigate } from 'react-router-dom';
import { useProductDetails } from '../../../hooks/products/useProduct';
import { LoadingIndicator } from '../../general/components/LoadingIndicator';

export const ProductDetails: React.FC = () => {
  const { productId } = useParams();
  const { productDetailsQuery } = useProductDetails(Number(productId));
  const { data, isLoading, isError } = productDetailsQuery;
  const navigate = useNavigate();

  const [isFavorite, setIsFavorite] = useState(false);
  const [showMore, setShowMore] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const [quantity, setQuantity] = useState(1);

  const handlePrevImage = () => {
    if (data?.product?.images) {
      setCurrentImageIndex((prev) =>
        prev === 0 ? data.product.images.length - 1 : prev - 1
      );
    }
  };

  const handleNextImage = () => {
    if (data?.product?.images) {
      setCurrentImageIndex((prev) =>
        prev === data.product.images.length - 1 ? 0 : prev + 1
      );
    }
  };

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

  if (!data.product) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <p className="text-red-600 text-xl mb-2">Product not found</p>
          <p className="text-gray-600">Please check the product ID and try again</p>
        </div>
      </div>
    );
  }

  const product = data.product;
  const inStock = product.stock > 0;

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-10">
      {/* Header */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Left Column - Product Image and Info */}
          <div className="bg-white rounded-3xl p-6 border border-pink-100">
            {/* Product Image */}
            <div className="bg-linear-to-br from-pink-50 to-cyan-50 rounded-2xl p-12 mb-6 flex items-center justify-center relative">
              <img
                src={product.images[currentImageIndex]?.image_url || 'https://placehold.co/600x400/f5f5f5/999999?text=Image+Unavailable&font=inter'}
                alt={`${product.product_name} - Image ${currentImageIndex + 1}`}
                className="w-full max-h-80 object-contain rounded-2xl"
              />

              {/* Navigation Buttons */}
              {product.images.length > 1 && (
                <>
                  <button
                    onClick={handlePrevImage}
                    className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/90 hover:bg-white p-2 rounded-full shadow-lg transition"
                  >
                    <ChevronLeft className="w-5 h-5 text-gray-800" />
                  </button>
                  <button
                    onClick={handleNextImage}
                    className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/90 hover:bg-white p-2 rounded-full shadow-lg transition"
                  >
                    <ChevronRight className="w-5 h-5 text-gray-800" />
                  </button>
                </>
              )}

              {/* Image Counter */}
              {product.images.length > 1 && (
                <div className="absolute top-4 left-4 bg-black/60 text-white px-3 py-1 rounded-full text-xs font-medium">
                  {currentImageIndex + 1} / {product.images.length}
                </div>
              )}

              {/* In Stock Badge */}
              {inStock && (
                <div className="absolute top-4 right-4 bg-green-500 text-white px-3 py-1.5 rounded-full font-semibold flex items-center gap-1.5 text-xs">
                  <Check className="w-3.5 h-3.5" />
                  In Stock
                </div>
              )}
              <div className="absolute top-4 left-4">
                <button
                  onClick={() => navigate(-1)}
                  className="p-2 hover:bg-gray-100 rounded-full transition cursor-pointer"
                >
                  <ArrowLeft className="w-6 h-6" />
                </button>
              </div>

              {/* Thumbnail Dots */}
              {product.images.length > 1 && (
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                  {product.images.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentImageIndex(index)}
                      className={`w-2 h-2 rounded-full transition ${index === currentImageIndex ? 'bg-pink-500 w-6' : 'bg-white/60 hover:bg-white'
                        }`}
                    />
                  ))}
                </div>
              )}
            </div>

            {/* Product Title and Price */}
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{product.product_name}</h1>
              <div className="flex gap-2">
                <button className="p-2 hover:bg-gray-100 rounded-full transition cursor-pointer">
                  <Share2 className="w-6 h-6" />
                </button>
                <button
                  onClick={() => setIsFavorite(!isFavorite)}
                  className="p-2 hover:bg-gray-100 rounded-full transition cursor-pointer"
                >
                  <Heart
                    className={`w-6 h-6 ${isFavorite ? 'fill-pink-500 text-pink-500' : ''}`}
                  />
                </button>
              </div>
            </div>
            <p className="text-4xl font-bold text-pink-500 mb-3">₱{product.base_price.toLocaleString()}</p>

            <div className="flex items-center gap-3 mb-6">
              <span className="text-gray-600 text-sm">{product.category.category_name}</span>
              <span className="text-blue-500 font-semibold text-sm">{product.stock} available</span>
            </div>

            {/* Product Highlights */}
            <div className="mb-6">
              <h2 className="text-base font-bold text-gray-900 mb-3">Product Highlights</h2>
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-pink-50 rounded-xl p-3 text-center">
                  <Shield className="w-5 h-5 text-pink-500 mx-auto mb-1" />
                  <span className="text-xs font-medium text-gray-700 block leading-tight">High quality materials</span>
                </div>
                <div className="bg-pink-50 rounded-xl p-3 text-center">
                  <Truck className="w-5 h-5 text-pink-500 mx-auto mb-1" />
                  <span className="text-xs font-medium text-gray-700 block leading-tight">Fast shipping available</span>
                </div>
                <div className="bg-pink-50 rounded-xl p-3 text-center">
                  <Package className="w-5 h-5 text-pink-500 mx-auto mb-1" />
                  <span className="text-xs font-medium text-gray-700 block leading-tight">Money back guarantee</span>
                </div>
              </div>
            </div>

            {/* Description */}
            <div>
              <h2 className="text-base font-bold text-gray-900 mb-2">Description</h2>
              <p className="text-gray-600 text-sm leading-relaxed">
                {showMore ? product.description : `${product.description?.slice(0, 80)}...`}
              </p>
              <button
                onClick={() => setShowMore(!showMore)}
                className="text-pink-500 font-semibold text-sm mt-2 hover:text-pink-600 transition"
              >
                {showMore ? 'See Less' : 'See More'}
              </button>
            </div>
          </div>

          {/* Right Column - Shop Info and Actions */}
          <div className="flex flex-col gap-4">
            {/* Shop Information */}
            <div className="bg-white border border-gray-200 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
                  <Store className="w-5 h-5 text-pink-500" />
                  Shop Information
                </h3>
                <button className="flex items-center gap-1 px-3 py-1.5 text-pink-500 font-semibold hover:bg-pink-50 rounded-lg transition cursor-pointer text-sm">
                  <Store className="w-4 h-4" />
                  Visit Shop
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>

              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-linear-to-br from-pink-400 to-pink-600 rounded-full flex items-center justify-center shrink-0">
                  <span className="text-white text-lg font-bold">{data.product.seller.business_name?.charAt(0).toUpperCase()}</span>
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 text-sm">{data.product.seller.business_name}</h4>
                  <p className="text-xs text-gray-500 flex items-center gap-1">
                    <span>📍</span>
                    {data.product.seller.business_address}
                  </p>
                </div>
              </div>

              <button className="w-full py-2.5 border-2 border-pink-500 text-pink-500 rounded-full font-semibold hover:bg-pink-50 transition cursor-pointer flex items-center justify-center gap-2 text-sm">
                <span>💬</span>
                Contact Seller
              </button>
            </div>

            {/* Important Information */}
            <div className="bg-blue-50 border border-blue-200 rounded-2xl p-5">
              <h3 className="text-base font-bold text-gray-900 mb-3 flex items-center gap-2">
                <span className="text-blue-500">ℹ️</span>
                Important Information
              </h3>
              <ul className="space-y-2 text-xs text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>Please check product details before purchasing</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>Contact Seller for bulk orders or customization</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>Returns accepted with 7 days of delivery</span>
                </li>
              </ul>
            </div>

            {/* Quantity Selector */}
            <div className="flex flex-row items-center justify-between bg-white border border-gray-200 rounded-2xl p-5">
              <h3 className="text-base font-semibold text-gray-900">Quantity</h3>
              <div className="flex items-center justify-center gap-4">
                <button
                  onClick={() => setQuantity((qty) => Math.max(1, qty - 1))}
                  className="w-10 h-10 bg-gray-100 text-gray-700 rounded-xl flex items-center justify-center hover:bg-gray-300 transition font-bold"
                >
                  -
                </button>
                <input
                  type="text"
                  value={quantity}
                  min={1}
                  onChange={(e) => setQuantity(Math.max(1, Number(e.target.value)))}
                  className="w-16 text-center text-gray-900 font-medium text-lg border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-500"
                />
                <button
                  onClick={() => setQuantity((qty) => qty + 1)}
                  className="w-10 h-10 bg-gray-100 text-gray-700 rounded-xl flex items-center justify-center hover:bg-gray-300 transition font-bold"
                >
                  +
                </button>
              </div>
            </div>



            {/* Action Buttons */}
            <div className="grid grid-cols-2 gap-3">
              <button className="flex items-center justify-center gap-2 px-4 py-3 border-2 border-pink-500 text-pink-500 rounded-full font-semibold hover:bg-pink-50 transition cursor-pointer text-sm">
                <ShoppingCart className="w-5 h-5" />
                Add to Cart
              </button>
              <button className="px-4 py-3 bg-linear-to-r from-pink-500 to-pink-600 text-white rounded-full font-semibold hover:from-pink-600 hover:to-pink-700 transition shadow-lg shadow-pink-500/30 cursor-pointer flex items-center justify-center gap-2 text-sm">
                <CreditCard className="w-5 h-5" />
                Buy Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ProductDetails;