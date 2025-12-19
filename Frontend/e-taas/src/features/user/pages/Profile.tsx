import { useCurrentUser } from "../../../store/currentUserStore";
import { LoadingIndicator } from "../../general/components/LoadingIndicator";
import { updateUserDetails } from "../../../services/user/UserDetails";
import type { UpdateUserData } from "../../../types/user/User";
import { useForm } from "../../../hooks/useForm";
import { useState } from "react";

export const Profile: React.FC = () => {

  const currentUser = useCurrentUser((state) => state.currentUser);
  const isLoading = useCurrentUser((state) => state.isLoading);
  const updateCurrentUser = useCurrentUser((state) => state.updateCurrentUser);
  const [isSaved, setIsSaved] = useState(false);
  const [toggleEdit, setToggleEdit] = useState(false);

  const { values, handleChange, reset } = useForm<UpdateUserData>({
    first_name: currentUser?.first_name || "",
    middle_name: currentUser?.middle_name || "",
    last_name: currentUser?.last_name || "",
    address: currentUser?.address || "",
    contact_number: currentUser?.contact_number || "",
  });

  const hasChanges = () => {
    return (
      values.first_name !== (currentUser?.first_name || "") ||
      values.middle_name !== (currentUser?.middle_name || "") ||
      values.last_name !== (currentUser?.last_name || "") ||
      values.address !== (currentUser?.address || "") ||
      values.contact_number !== (currentUser?.contact_number || "")
    );
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!hasChanges()) {
      setToggleEdit(false);
      return;
    }

    try {
      const updatedUser = await updateUserDetails(values);
      updateCurrentUser(updatedUser);
      setIsSaved(true);
      setToggleEdit(false);
      setTimeout(() => setIsSaved(false), 3000);
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  const handleCancel = () => {
    reset();
    setToggleEdit(false);
    setIsSaved(false);
  };

  if (isLoading && !currentUser) {
    return <LoadingIndicator />;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto flex gap-6">
        {/* Left Sidebar */}
        <div className="w-1/3 bg-white rounded-3xl shadow-sm p-8 space-y-6">
          {/* User Info */}
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-pink-500 flex items-center justify-center text-white text-2xl font-semibold">
              {currentUser?.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="font-semibold text-gray-900">{currentUser?.username}</div>
              <div className="text-sm text-gray-500">{currentUser?.email}</div>
            </div>
          </div>

          {/* Become a seller button */}
          <button className="w-full border border-pink-200 rounded-lg py-3 px-4 flex items-center justify-between text-pink-500 hover:bg-pink-50 transition cursor-pointer">
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

          {/* My Purchases Section */}
          <div className="space-y-6">
            <h3 className="font-semibold text-gray-900 mb-4">My Purchases</h3>

            <button className="w-full border border-gray-200 rounded-lg py-4 px-4 flex items-center justify-between hover:bg-gray-50 transition cursor-pointer ">
              <div className="flex items-center gap-3">
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                <span className="text-gray-900">My orders</span>
              </div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button className="w-full border border-gray-200 rounded-lg py-4 px-4 flex items-center justify-between hover:bg-gray-50 transition cursor-pointer">
              <div className="flex items-center gap-3">
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                <span className="text-gray-900">To Ship</span>
              </div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button className="w-full border border-gray-200 rounded-lg py-4 px-4 flex items-center justify-between hover:bg-gray-50 transition cursor-pointer">
              <div className="flex items-center gap-3">
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                </svg>
                <span className="text-gray-900">To Receive</span>
              </div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button className="w-full border border-gray-200 rounded-lg py-4 px-4 flex items-center justify-between hover:bg-gray-50 transition cursor-pointer">
              <div className="flex items-center gap-3">
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-gray-900">My Purchase History</span>
              </div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        {/* Right Panel - Account Details */}
        <div className="flex-1 bg-white rounded-3xl shadow-sm p-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-8">Account Details</h2>

          <form onSubmit={handleSave} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Name*
              </label>
              <input
                type="text"
                name="first_name"
                onChange={handleChange}
                value={values.first_name}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                disabled={!toggleEdit}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Middle Name
              </label>
              <input
                type="text"
                name="middle_name"
                value={values.middle_name}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                disabled={!toggleEdit}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Last Name*
              </label>
              <input
                type="text"
                name="last_name"
                value={values.last_name}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                disabled={!toggleEdit}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Address*
              </label>
              <input
                type="text"
                name="address"
                value={values.address}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                disabled={!toggleEdit}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contact Number*
              </label>
              <input
                type="text"
                name="contact_number"
                value={values.contact_number}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                disabled={!toggleEdit}
              />
            </div>

            <div className="flex items-center gap-4 mt-6">
              {!toggleEdit ? (
                <button
                  type="button"
                  onClick={() => setToggleEdit(true)}
                  className="px-6 py-3 rounded-lg font-semibold text-white bg-pink-500 hover:bg-pink-600 transition"
                >
                  Edit Profile
                </button>
              ) : (
                <>
                  <button
                    type="submit"
                    className="px-6 py-3 rounded-lg font-semibold text-white bg-pink-500 hover:bg-pink-600 transition"
                  >
                    Save Changes
                  </button>
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="px-6 py-3 rounded-lg font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 transition"
                  >
                    Cancel
                  </button>
                </>
              )}
              {isSaved && <span className="text-pink-600 font-medium">Profile updated successfully!</span>}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}