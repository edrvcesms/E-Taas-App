import React from "react"

interface ConfirmationModalProps {
  open: boolean
  title: string
  description: string
  onCancel: () => void
  onConfirm: () => void
}

export const ConfirmationModal: React.FC<ConfirmationModalProps> = ({
  open,
  title,
  description,
  onCancel,
  onConfirm,
}) => {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-transparent">
      <div className="w-full max-w-sm rounded-lg bg-pink-500 p-6">
        <h2 className="text-lg font-semibold text-white">
          {title}
        </h2>

        <p className="mt-2 text-sm text-white">
          {description}
        </p>

        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={onCancel}
            className="rounded-md border border-white px-4 py-2 text-white hover:bg-pink-600/20 cursor-pointer"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            className="rounded-md bg-white px-4 py-2 text-pink-500 hover:bg-pink-100 cursor-pointer"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  )
}
