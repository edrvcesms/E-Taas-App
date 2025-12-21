import { useCurrentUser } from "../../../store/currentUserStore";
import { LoadingIndicator } from "../../general/components/LoadingIndicator";
import UserDetailsForm from "../components/UserDetailsForm";
import { SwitchRoleButton } from "../components/SwitchRoleButton";
import { Button } from "../../general/components/Buttons";

export const Profile: React.FC = () => {
  const currentUser = useCurrentUser((state) => state.currentUser);
  const isLoading = useCurrentUser((state) => state.isLoading);
  
  if (isLoading && !currentUser) {
    return <LoadingIndicator />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-500/5 to-white p-8">
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
            <h3 className="font-semibold text-gray-900 mb-4">My Purchases</h3>

            <Button {...{
              onClick: () => {},
              label: "To Ship",
              icon: (
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              )
            }} />

            <Button {...{
              onClick: () => {},
              label: "To Receive",
              icon: (
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                </svg>
              )
            }} />

            <Button {...{
              onClick: () => {},
              label: "My Purchase History",
              icon: (
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                </svg>
              )
            }} />
            <Button {...{
              onClick: () => {},
              label: "My Purchase History",
              icon: (
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )
            }} />
          </div>

          {/* Account Stats */}
          <div className="pt-6 border-t border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4">Account Stats</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-pink-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-pink-500">24</div>
                <div className="text-xs text-gray-600 mt-1">Total Orders</div>
              </div>
              <div className="bg-pink-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-pink-500">12</div>
                <div className="text-xs text-gray-600 mt-1">Wishlist Items</div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="pt-6 border-t border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <Button {...{
                onClick: () => {},
                label: "My Wishlist",
                icon: (
                  <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                )
              }} />
              <Button {...{
                onClick: () => {},
                label: "My Vouchers",
                icon: (
                  <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
                  </svg>
                )
              }} />
              <Button {...{
                onClick: () => {},
                label: "Account Settings",
                icon: (
                  <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                )
              }} />
            </div>
          </div>
        </div>
        
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
};