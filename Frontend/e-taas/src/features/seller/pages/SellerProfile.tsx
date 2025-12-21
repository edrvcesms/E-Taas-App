import { useCurrentUser } from "../../../store/currentUserStore";
import { LoadingIndicator } from "../../general/components/LoadingIndicator";
import UserDetailsForm from "../../user/components/UserDetailsForm";
import { Button } from "../../general/components/Buttons";
import { SwitchRoleButton } from "../../user/components/SwitchRoleButton";

export const SellerProfile: React.FC = () => {
  const currentUser = useCurrentUser((state) => state.currentUser);
  const isLoading = useCurrentUser((state) => state.isLoading);

  if (isLoading && !currentUser) {
    return <LoadingIndicator />;
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-pink-500/5 to-white p-8">
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

          {/* My Purchases Section */}
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

          {/* Account Stats */}
          <div className="pt-6 border-t border-gray-100">
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

        {/* Right Content Area */}
        <div className="flex-1 space-y-6">
          <UserDetailsForm />
          
          {/* Recent Activity */}
          <div className="bg-white rounded-3xl shadow-sm p-8">
            <h3 className="font-semibold text-gray-900 mb-6">Recent Activity</h3>
            <div className="space-y-4">
              <div className="flex items-start gap-4 pb-4 border-b border-gray-100">
                <div className="w-12 h-12 rounded-lg bg-pink-100 flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Order Placed</div>
                  <div className="text-sm text-gray-500 mt-1">Your order #12345 has been confirmed</div>
                  <div className="text-xs text-gray-400 mt-2">2 hours ago</div>
                </div>
              </div>
              
              <div className="flex items-start gap-4 pb-4 border-b border-gray-100">
                <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Delivery Complete</div>
                  <div className="text-sm text-gray-500 mt-1">Order #12340 has been delivered</div>
                  <div className="text-xs text-gray-400 mt-2">Yesterday</div>
                </div>
              </div>
              
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">New Voucher</div>
                  <div className="text-sm text-gray-500 mt-1">You received a 20% off voucher</div>
                  <div className="text-xs text-gray-400 mt-2">3 days ago</div>
                </div>
              </div>
            </div>
          </div>

          {/* Saved Addresses */}
          <div className="bg-white rounded-3xl shadow-sm p-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-gray-900">Saved Addresses</h3>
              <button className="text-sm text-pink-500 hover:text-pink-600">+ Add New</button>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="border border-gray-200 rounded-lg p-4 hover:border-pink-300 transition cursor-pointer">
                <div className="flex items-start justify-between mb-2">
                  <span className="text-xs bg-pink-100 text-pink-600 px-2 py-1 rounded">Default</span>
                  <button className="text-gray-400 hover:text-gray-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                  </button>
                </div>
                <div className="text-sm font-medium text-gray-900 mb-1">Home</div>
                <div className="text-xs text-gray-500">123 Main St, Apt 4B, New York, NY 10001</div>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4 hover:border-pink-300 transition cursor-pointer">
                <div className="flex items-start justify-between mb-2">
                  <div className="h-5"></div>
                  <button className="text-gray-400 hover:text-gray-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                  </button>
                </div>
                <div className="text-sm font-medium text-gray-900 mb-1">Office</div>
                <div className="text-xs text-gray-500">456 Business Ave, Floor 12, New York, NY 10002</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}