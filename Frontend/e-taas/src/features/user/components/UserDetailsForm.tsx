import React from 'react'
import { useState } from 'react';
import { useForm } from '../../../hooks/useForm';
import type { UpdateUserData } from '../../../types/user/User';
import { useCurrentUser } from '../../../store/currentUserStore';
import { updateUserDetails } from '../../../services/user/UserDetails';

const UserDetailsForm: React.FC = () => {

  const currentUser = useCurrentUser((state) => state.currentUser);
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

  return (
    <>
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
    </>
  )
}

export default UserDetailsForm