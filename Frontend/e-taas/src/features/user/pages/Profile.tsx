import { useCurrentUser } from "../../../store/currentUserStore";
import { LoadingIndicator } from "../../general/components/LoadingIndicator";

export const Profile: React.FC = () => {
  
  const currentUser = useCurrentUser((state) => state.currentUser);

  return (
    <>
      <div className="min-h-screen bg-linear-to-br from-pink-50 via-white to-pink-100 flex items-center justify-center p-4">
        <div className="w-full max-w-4xl">
          <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
            <div className="text-center space-y-2">
              <h1 className="text-3xl font-bold text-pink-500">User Profile</h1>
              <p className="text-gray-500">View and manage your profile information</p>
            </div>
            {currentUser ? (
              <div className="space-y-4">
                <div>
                  <h2 className="text-xl font-semibold">Username:</h2>
                  <p className="text-gray-700">{currentUser.username}</p>
                </div>
                <div>
                  <h2 className="text-xl font-semibold">Email:</h2>
                  <p className="text-gray-700">{currentUser.email}</p>
                </div>
                <div>
                  <h2 className="text-xl font-semibold">Contact Number:</h2>
                  <p className="text-gray-700">{currentUser.contact_number || "N/A"}</p>
                </div>
                <div>
                  <h2 className="text-xl font-semibold">Role:</h2>
                  <p className="text-gray-700">
                    {currentUser.is_admin
                      ? "Admin"
                      : currentUser.is_seller
                      ? "Seller"
                      : "Buyer"}
                  </p>
                </div>
              </div>
            ) : (
              <LoadingIndicator />
            )}
          </div>
        </div>
      </div>
    </>
  );
}
