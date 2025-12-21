import { useCurrentUser } from "../../../store/currentUserStore";
import { useSwitchRole } from "../../../hooks/useSwitchRole";
import { useNavigate } from "react-router-dom";
import { ConfirmationModal } from "../../general/components/ConfirmationModal";
import { useState } from "react";

export const SwitchRoleButton: React.FC = () => {
  const { isSellerMode, toggleRole } = useSwitchRole();
  const currentUser = useCurrentUser((state) => state.currentUser);
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSwitch = async () => {
    await toggleRole();
  };

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  return (
    <>
      {/* Become a seller button */}
      {currentUser && !currentUser.is_seller ? (
        <button
          onClick={() => navigate("/seller-application")}
          className="w-full border border-pink-200 rounded-lg py-3 px-4 flex items-center justify-between text-pink-500 hover:bg-pink-50 transition cursor-pointer"
        >
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <span>Become a seller?</span>
          </div>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      ) : (
        <button
          onClick={toggleModal}
          className={`w-full border rounded-lg py-3 px-4 flex items-center justify-between transition cursor-pointer ${isSellerMode
              ? "border-pink-500 text-pink-500 bg-pink-50 hover:bg-pink-100"
              : "border-white-500 text-white bg-pink-500 hover:bg-pink-500/90"
            }`}
        >
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <span>{isSellerMode ? "Switch to Buyer Mode" : "Switch to Seller Mode"}</span>
          </div>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      )}
      <ConfirmationModal
        open={isModalOpen}
        title="Confirm Role Switch"
        description={`Are you sure you want to switch to ${isSellerMode ? "Buyer" : "Seller"} Mode?`}
        onCancel={toggleModal}
        onConfirm={async () => {
          await handleSwitch();
          toggleModal();
        }}
      />
    </>
  )
}