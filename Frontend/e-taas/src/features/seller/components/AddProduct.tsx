import { useSellerProduct } from "../../../hooks/seller/useSellerProduct";
import type { ProductData } from "../../../types/products/ManageProduct";
import { useState } from "react";
import { addImageToProduct } from "../../../services/products/ManageProducts";
import { useForm } from "../../../hooks/general/useForm";

export const AddProduct: React.FC = () => {

  const { values: formData, setValues: setFormData, handleChange } = useForm<ProductData>({
    product: {
      product_name: "",
      description: "",
      base_price: 0,
      stock: 0,
      has_variants: false,
      category_id: 0,
    },
    variant_categories: [],
    variants: [],
  });

  const [selectedImages, setSelectedImages] = useState<File[]>([]);
  const { addNewProductMutation } = useSellerProduct();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files);
      setSelectedImages(prev => [...prev, ...newFiles]);
    }
  };

  const handleRemoveImage = (indexToRemove: number) => {
    setSelectedImages(prev => prev.filter((_, index) => index !== indexToRemove));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const newProduct = await addNewProductMutation.mutateAsync(formData);

      if (selectedImages.length > 0) {
        const imageFormData = new FormData();
        selectedImages.forEach((image) => {
          imageFormData.append("images", image);
        });
        try {
          await addImageToProduct(imageFormData, newProduct.product.id);
        } catch (error) {
          console.error("Error uploading images:", error);
        }
      }
      setSelectedImages([]);
      setFormData({
        product: {
          product_name: "",
          description: "",
          base_price: 0,
          stock: 0,
          has_variants: false,
          category_id: 0,
        },
        variant_categories: [],
        variants: [],
      });
    } catch (error) {
      console.error("Error adding product:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-md rounded-md mt-10 py-40">
      <h2 className="text-2xl font-bold mb-6 text-pink-500">Manage Products</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Product Name
          </label>
          <input
            type="text"
            name="product.product_name"
            value={formData.product.product_name}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            name="product.description"
            value={formData.product.description}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Base Price
          </label>
          <input
            type="number"
            name="product.base_price"
            value={formData.product.base_price}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Stock
          </label>
          <input
            type="number"
            name="product.stock"
            value={formData.product.stock}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Category ID
          </label>
          <input
            type="number"
            name="product.category_id"
            value={formData.product.category_id}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Product Images
          </label>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={handleImageChange}
            className="mt-1 block w-full"
          />
          <p className="mt-1 text-sm text-gray-500">
            You can select multiple images. Click "Choose Files" again to add more.
          </p>
        </div>
        {selectedImages.length > 0 && (
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-700 mb-2">
              Selected Images ({selectedImages.length})
            </p>
            <div className="grid grid-cols-3 gap-4">
              {selectedImages.map((image, index) => (
                <div key={index} className="relative border border-gray-300 rounded-md p-2">
                  <img
                    src={URL.createObjectURL(image)}
                    alt={`Selected ${index + 1}`}
                    className="w-full h-32 object-cover rounded-md"
                  />
                  <button
                    type="button"
                    onClick={() => handleRemoveImage(index)}
                    className="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600 transition-colors"
                    aria-label="Remove image"
                  >
                    ×
                  </button>
                  <p className="text-xs text-gray-600 mt-1 truncate">
                    {image.name}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
        <button
          type="submit"
          disabled={isSubmitting}
          className="bg-pink-500 text-white px-4 py-2 rounded-md hover:bg-pink-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isSubmitting ? "Submitting..." : "Add Product"}
        </button>
      </form>
    </div>
  );

}