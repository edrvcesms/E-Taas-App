import { getAllProducts } from "../../../services/products/Products";
import { useEffect, useState } from "react";
import { addProduct } from "../../../services/products/ManageProducts";
import type { ProductData } from "../../../types/products/Products";
import { addImageToProduct } from "../../../services/products/ManageProducts";

export const Products: React.FC = () => {

  const [selectedFiles, setSelectedFiles] = useState<File[]>([])



  const newProduct: ProductData = {
    product: {
      product_name: "Sample Product",
      description: "This is a sample product.",
      base_price: 29.99,
      stock: 100,
      has_variants: true,
      category_id: 1,
    }, variant_categories: [
        {
          category_name: "Size",
          attributes: [
            { value: "Small" },
            { value: "Medium" },
            { value: "Large" }
          ]
        },
        {
          category_name: "Color",
          attributes: [
            { value: "Red" },
            { value: "Blue" },
            { value: "Green" }
          ]
        }
      ],
      variants: [{ stock: 50, price: 29.99 }]
  };

const handleSubmit = async () => {
  try {
    const products = await addProduct(newProduct)
      if (products && products.product && products.product.id && selectedFiles.length > 0) {
        const productId = products.product.id
        const formData = new FormData()
        selectedFiles.forEach(file => formData.append("images", file))
      await addImageToProduct(formData, productId)
      console.log("Product and images added successfully")
    }
  } catch (err) {
    console.error(err)
  }
}

  return (
    <>
      <div className="text-3xl">Products Page</div>
        <input
          type="file"
          multiple
          onChange={(e) => {
            if (!e.target.files) return
            const incoming = Array.from(e.target.files)
            setSelectedFiles(prev => [...prev, ...incoming])
          }}
        />

        <div className="mt-2 flex gap-2">
          {selectedFiles.map((file, idx) => (
            <img
              key={idx}
              src={URL.createObjectURL(file)}
              alt={file.name}
              className="w-20 h-20 object-cover rounded"
            />
          ))}
        </div>

        <button
          onClick={handleSubmit}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Add Product
        </button>
      </>

  );
}
