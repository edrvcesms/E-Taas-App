import React, { useState } from 'react'
import { productApi } from '../../../services/axios/ApiServices'

type VariantData = {
  variant_id: number
  price: number
  stock: number
  remove_image?: boolean
}

const variantList: VariantData[] = [
  { variant_id: 1, price: 100, stock: 50 },
  { variant_id: 2, price: 150, stock: 30 },
  { variant_id: 4, price: 200, stock: 20 }
]

const ManageProductPage = () => {
  const [variantFiles, setVariantFiles] = useState<Record<number, File[]>>({})

  function handleFileChange(variantId: number, e: React.ChangeEvent<HTMLInputElement>) {
    const target = e.target as HTMLInputElement
    if (!target.files) return
    setVariantFiles(prev => ({
      ...prev,
      [variantId]: Array.from(target.files ?? [])
    }))

  }

  function handleRemoveFile(variantId: number) {
    setVariantFiles(prev => ({ ...prev, [variantId]: [] }))
  }

  async function bulkUpdateVariants() {
    const formData = new FormData()

    // Build arrays for files and their variant IDs
    const allFiles: File[] = []
    const variantIdMap: number[] = []

    Object.entries(variantFiles).forEach(([variantIdStr, files]) => {
      const variantId = Number(variantIdStr)
      files.forEach(file => {
        allFiles.push(file)
        variantIdMap.push(variantId)
      })
    })

    // Append files
    allFiles.forEach(file => formData.append("files", file))

    // Append variant IDs matching the file order
    formData.append("variant_ids", JSON.stringify(variantIdMap))

    // Build variant data with remove_image flag
    const preparedVariantData = variantList.map(variant => ({
      ...variant,
      remove_image: !variantFiles[variant.variant_id]?.length
    }))
    formData.append("variant_data", JSON.stringify(preparedVariantData))

    try {
      const response = await productApi.put("/update-variants", formData, {
        withCredentials: true
      })
      console.log(response.data)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className='py-50'>
      {variantList.map(variant => (
        <div key={variant.variant_id} className='mb-6'>
          <h3>Variant {variant.variant_id}</h3>
          <input
            type='file'
            multiple
            onChange={e => handleFileChange(variant.variant_id, e)}
          />
          <button
            type='button'
            className='ml-2 px-2 py-1 bg-gray-300 rounded'
            onClick={() => handleRemoveFile(variant.variant_id)}
          >
            Clear Files
          </button>
          <div className='flex gap-2 mt-2'>
            {variantFiles[variant.variant_id]?.map((file, idx) => (
              <img
                key={idx}
                src={URL.createObjectURL(file)}
                alt={file.name}
                className='w-24 h-24 object-cover border'
              />
            ))}
          </div>
        </div>
      ))}

      <button
        className='mt-4 px-4 py-2 bg-pink-500 text-white rounded'
        onClick={bulkUpdateVariants}
      >
        Upload
      </button>
    </div>
  )
}

export default ManageProductPage
