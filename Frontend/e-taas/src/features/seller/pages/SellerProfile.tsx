import { useCurrentUser } from "../../../store/currentUserStore";
import { LoadingIndicator } from "../../general/components/LoadingIndicator";
import { Button } from "../../general/components/Buttons";
import { SwitchRoleButton } from "../../user/components/SwitchRoleButton";

export const SellerProfile: React.FC = () => {
  const currentUser = useCurrentUser((state) => state.currentUser);
  const isLoading = useCurrentUser((state) => state.isLoading);

  if (isLoading && !currentUser) {
    return <LoadingIndicator />;
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-50 to-white p-8">
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

          <SwitchRoleButton />

          {/* Business Management Section */}
          <div className="space-y-6">
            <h3 className="font-semibold text-gray-900 mb-4">Business Management</h3>

            <Button 
              onClick={() => {}}
              label="My Products"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              }
            />

            <Button
              onClick={() => {}}
              label="Orders Management"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              }
            />

            <Button 
              onClick={() => {}}
              label="Sales Analytics"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 11V9a4 4 0 114 4h-2a2 2 0 10-2-2zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              }
            />

            <Button 
              onClick={() => {}}
              label="Customer Inquiries"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16h6m-7 4h8a2 2 0 002-2V6a2 2 0 00-2-2H7a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              }
            />
          </div>

          {/* Analytics & Insights */}
          <div className="pt-6 border-t border-gray-100 space-y-6">
            <h3 className="font-semibold text-gray-900 mb-4">Analytics & Insights</h3>
            <Button 
              onClick={() => {}}
              label="View Revenue Reports"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 17a2 2 0 104 0v-5a2 2 0 10-4 0v5zm-7 4a9 9 0 1118 0H4z" />
                </svg>
              }
            />
            <Button
              onClick={() => {}}
              label="Customer Reviews"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                </svg>
              }
            />

            <Button 
              onClick={() => {}}
              label="Inventory Alerts"
              icon={
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-4m4 0h-4m4 0h-4m-4 0H8m4 0H8m4 0H8" />
                </svg>
              }
            />
          </div>
        </div>

        {/* Right Content Area - Shop Profile Card */}
        <div className="flex-1">
          <div className="bg-white rounded-3xl shadow-sm overflow-hidden">
            {/* Cover Photo */}
            <div className="relative h-48 bg-linear-to-br from-pink-500 to-pink-600 flex items-center justify-center">
              <span className="text-white text-sm">Cover Photo</span>
            </div>

            {/* Shop Profile Content */}
            <div className="p-8">
              {/* Shop Avatar & Edit Button */}
              <div className="flex items-start justify-between mb-6">
                <div className="relative -mt-20">
                  <div className="w-28 h-28 rounded-full bg-pink-500 flex items-center justify-center text-white text-4xl font-bold border-4 border-white shadow-lg">
                    {currentUser?.username.charAt(0).toUpperCase()}
                  </div>
                  <button className="absolute bottom-1 right-1 w-8 h-8 bg-white rounded-full shadow-md flex items-center justify-center hover:bg-gray-50 transition">
                    <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                </div>

                <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition">
                  <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  <span className="text-sm font-medium text-gray-700">Edit Shop</span>
                </button>
              </div>

              {/* Shop Name */}
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {currentUser?.seller?.display_name}
              </h2>

              {/* Rating */}
              <div className="flex items-center gap-2 mb-3">
                <svg className="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
                <span className="text-lg font-semibold text-gray-900">{currentUser?.seller?.ratings}</span>
              </div>

              {/* Location */}
              <div className="flex items-center gap-2 text-gray-600 mb-3">
                <svg className="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                </svg>
                <span className="text-sm">{currentUser?.seller?.business_address}</span>
              </div>

              {/* Description */}
              <p className="text-gray-600 text-sm mb-6">
                Welcome to {currentUser?.seller?.display_name}'s Store! We offer a variety of products to meet your needs. Browse our collection and enjoy a seamless shopping experience.
              </p>

              {/* Contact Information */}
              <div className="flex items-center justify-between pt-6 border-t border-gray-100">
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span className="text-sm text-gray-600">{currentUser?.seller?.business_contact}</span>
                </div>

                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span className="text-sm text-gray-600">{currentUser?.email}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Shop Statistics */}
          <div className="mt-6 grid grid-cols-3 gap-4">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <div className="text-3xl font-bold text-gray-900 mb-1">0</div>
              <div className="text-sm text-gray-500">Total Products</div>
            </div>
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <div className="text-3xl font-bold text-gray-900 mb-1">0</div>
              <div className="text-sm text-gray-500">Total Sales</div>
            </div>
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <div className="text-3xl font-bold text-gray-900 mb-1">0</div>
              <div className="text-sm text-gray-500">Active Orders</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}