import { useProduct } from "../../../hooks/products/useProduct";
import { LoadingIndicator } from "../../general/components/LoadingIndicator";
import { useNavigate } from "react-router-dom";
import { useProductCategoryStore } from "../../../store/useProductCategoryStore";
import { useProductCategories } from "../../../hooks/products/useProductCategory";
import { Package, CheckCircle, AlertCircle, Tag, Eye, Edit, Trash2, Plus } from "lucide-react";

export const ManageProductPage = () => {
  const { allProductsQuery } = useProduct();
  const { data: products, isLoading, isError } = allProductsQuery;
  const navigate = useNavigate();
  const { productCategoriesQuery } = useProductCategories();
  const { data: productCategories, isLoading: isCategoriesLoading, isError: isCategoriesError } = productCategoriesQuery;
  
  if (isLoading || isCategoriesLoading) {
    return <LoadingIndicator />;
  }

  const handleAddProduct = () => {
    navigate("/add-product");
  }

  const toggleCategoryFilter = (categoryId: number) => {

  }


  if (isError || isCategoriesError) {
    return <div>Error loading products. Please try again later.</div>;
  }

  const totalProducts = products ? products.length : 0;
  const inStock = products ? products.filter(product => product.stock > 0).length : 0;
  const outOfStock = products ? products.filter(product => product.stock === 0).length : 0;
  const totalValue = products
    ? products.reduce((total, product) => total + product.base_price * product.stock, 0)
    : 0;

  return (
    <div className="min-h-screen bg-gray-50 p-6 py-30">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Manage Product</h1>
            <p className="text-gray-600">Track and manage your inventory</p>
          </div>
          <button 
            onClick={handleAddProduct}
            className="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-lg flex items-center gap-2 font-medium shadow-sm transition-colors"
          >
            <Plus size={20} />
            Add Product
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <span className="text-gray-600 text-sm font-medium">TOTAL PRODUCTS</span>
              <Package className="text-pink-500" size={24} />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{totalProducts}</div>
            <div className="text-gray-500 text-sm">All Items</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <span className="text-gray-600 text-sm font-medium">IN STOCK</span>
              <CheckCircle className="text-pink-500" size={24} />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{inStock}</div>
            <div className="text-gray-500 text-sm">Available</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <span className="text-gray-600 text-sm font-medium">OUT OF STOCK</span>
              <AlertCircle className="text-pink-500" size={24} />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{outOfStock}</div>
            <div className="text-gray-500 text-sm">Needs Restock</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-3">
              <span className="text-gray-600 text-sm font-medium">TOTAL VALUE</span>
              <Tag className="text-pink-500" size={24} />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              ₱{totalValue.toLocaleString('en-PH', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </div>
            <div className="text-gray-500 text-sm">Inventory Worth</div>
          </div>
        </div>

        {/* Products Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-1">My Products</h2>
            <p className="text-gray-600">Manage all of your products</p>
          </div>

          {/* Category Filters */}
          <div className="mb-6">
            <label className="text-sm font-medium text-gray-700 mb-3 block">Category</label>
            <div className="flex flex-wrap gap-2">
              <button className="px-6 py-2 bg-pink-500 text-white rounded-full font-medium hover:bg-pink-600 transition-colors">
                All
              </button>
              {productCategories && productCategories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => toggleCategoryFilter(category.id)}
                  className="px-6 py-2 bg-white text-pink-500 border border-pink-500 rounded-full font-medium hover:bg-pink-50 transition-colors"
                >
                  {category.category_name}
                </button>
              ))}
            </div>
          </div>

          {/* Availability Filters */}
          <div className="mb-6">
            <label className="text-sm font-medium text-gray-700 mb-3 block">Availability</label>
            <div className="flex flex-wrap gap-2">
              <button className="px-6 py-2 bg-pink-500 text-white rounded-full font-medium hover:bg-pink-600 transition-colors">
                All
              </button>
              <button className="px-6 py-2 bg-white text-pink-500 border border-pink-500 rounded-full font-medium hover:bg-pink-50 transition-colors">
                In Stock
              </button>
              <button className="px-6 py-2 bg-white text-pink-500 border border-pink-500 rounded-full font-medium hover:bg-pink-50 transition-colors">
                Out of Stock
              </button>
            </div>
          </div>

          {/* Products List */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Products ({totalProducts})</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {products && products.map((product) => (
                <div key={product.id} className="border border-gray-200 rounded-lg p-4 flex items-center gap-4 hover:shadow-md transition-shadow">
                  <img 
                    src={product.images[0]?.image_url || "https://placehold.co/100x100/f5f5f5/999999?text=No+Image&font=inter"} 
                    alt={product.product_name}
                    className="w-24 h-24 object-cover rounded-lg bg-gray-100"
                  />
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-1">{product.product_name}</h4>
                    <p className="text-sm text-gray-600 mb-2">{product.category.category_name}</p>
                    <p className="text-sm text-gray-600">
                      Quantity: {product.stock} - {product.stock > 0 ? 'In Stock' : 'Out of Stock'}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="p-2 text-gray-600 hover:text-gray-900 transition-colors">
                      <Eye size={20} />
                    </button>
                    <button className="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors flex items-center gap-2">
                      <Edit size={16} />
                      Edit
                    </button>
                    <button className="px-4 py-2 bg-white text-pink-500 border border-pink-500 rounded-lg hover:bg-pink-50 transition-colors flex items-center gap-2">
                      <Trash2 size={16} />
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}