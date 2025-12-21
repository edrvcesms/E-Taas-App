import type { SellerApplicationData } from "../../../types/seller/Application";
import { submitSellerApplication } from "../../../services/seller/Application";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "../../../hooks/useForm";
import { useCurrentUser } from "../../../store/currentUserStore";
import { User, Mail, Phone, Building2, Store, MapPin, Home } from "lucide-react";

export const SellerApplication = () => {
  const navigate = useNavigate();
  
  const { values, handleChange, reset } = useForm<SellerApplicationData>({
    business_name: "",
    business_address: "",
    business_contact: "",
    display_name: "",
    owner_address: ""
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<SellerApplicationData | null>(null);
  const currentUser = useCurrentUser((state) => state.currentUser);
  const updateCurrentUser = useCurrentUser((state) => state.updateCurrentUser);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    try {
      const application = await submitSellerApplication(values);
      updateCurrentUser({ is_seller: true, seller: application });
      navigate("/profile");
    } catch (err: any) {
      if (err.response && err.response.data) {
        setError(err.response.data);
      } else {
        console.error("Submission error:", err);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-8 py-30">
      <div className="max-w-7xl mx-auto px-4 mt-10">
        {/* Welcome Card */}
        <div className="bg-linear-to-br from-pink-500 to-pink-600 rounded-2xl p-6 mb-6 text-white shadow-lg">
          <div className="flex items-start gap-4 mb-4">
            <div className="bg-white/20 p-3 rounded-xl">
              <Store className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold mb-1">Become a Seller</h2>
              <p className="text-pink-100">Join E-Taas marketplace</p>
            </div>
          </div>
          <p className="text-sm text-pink-50 leading-relaxed">
            Complete the form below to register your business and start reaching thousands of customers on our platform.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Personal Information Section */}
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
              Personal Information
            </h3>
            
            <div className="space-y-4">
              {/* Full Name */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <User className="w-5 h-5 text-pink-500" />
                  Full Name *
                </label>
                <input
                  type="text"
                  value={currentUser?.first_name + " " + currentUser?.last_name || ""}
                  disabled
                  className="w-full px-4 py-3 bg-gray-50 text-gray-900 rounded-lg border-0 focus:outline-none"
                />
              </div>

              {/* Email Address */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <Mail className="w-5 h-5 text-pink-500" />
                  Email Address *
                </label>
                <input
                  type="text"
                  value={currentUser?.email || ""}
                  disabled
                  className="w-full px-4 py-3 bg-gray-50 text-gray-900 rounded-lg border-0 focus:outline-none"
                />
              </div>

              {/* Contact Number */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <Phone className="w-5 h-5 text-pink-500" />
                  Contact Number *
                </label>
                <input
                  type="text"
                  value={currentUser?.contact_number || ""}
                  disabled
                  className="w-full px-4 py-3 bg-gray-50 text-gray-900 rounded-lg border-0 focus:outline-none"
                />
              </div>
              {/* Owner Address */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <Home className="w-5 h-5 text-pink-500" />
                  Owner Address *
                </label>
                <input
                  type="text"
                  id="owner_address"
                  name="owner_address"
                  value={currentUser?.address || values.owner_address}
                  onChange={handleChange}
                  placeholder="123 Home St., City"
                  className={`w-full px-4 py-3 rounded-lg border-0 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:bg-white ${
                    error?.owner_address ? "ring-2 ring-red-500" : ""
                  }`}
                  required
                />
                {error?.owner_address && (
                  <p className="text-red-500 text-sm mt-2">{error.owner_address}</p>
                )}
              </div>
            </div>
          </div>

          {/* Business Information Section */}
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
              Business Information
            </h3>
            
            <div className="space-y-4">
              {/* Business Name */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <Building2 className="w-5 h-5 text-pink-500" />
                  Business Name *
                </label>
                <input
                  type="text"
                  id="business_name"
                  name="business_name"
                  value={values.business_name}
                  onChange={handleChange}
                  placeholder="ABC Trading Company"
                  className={`w-full px-4 py-3 rounded-lg border-0 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:bg-white ${
                    error?.business_name ? "ring-2 ring-red-500" : ""
                  }`}
                  required
                />
                {error?.business_name && (
                  <p className="text-red-500 text-sm mt-2">{error.business_name}</p>
                )}
              </div>

              {/* Shop Display Name */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-1">
                  <Store className="w-5 h-5 text-pink-500" />
                  Shop Display Name *
                </label>
                <p className="text-xs text-gray-500 mb-3 ml-8">
                  This is how your shop will appear to customers
                </p>
                <input
                  type="text"
                  id="display_name"
                  name="display_name"
                  value={values.display_name}
                  onChange={handleChange}
                  placeholder="John's Amazing Store"
                  className={`w-full px-4 py-3 rounded-lg border-0 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:bg-white ${
                    error?.display_name ? "ring-2 ring-red-500" : ""
                  }`}
                  required
                />
                {error?.display_name && (
                  <p className="text-red-500 text-sm mt-2">{error.display_name}</p>
                )}
              </div>

              {/* Business Address */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <MapPin className="w-5 h-5 text-pink-500" />
                  Business Address *
                </label>
                <input
                  type="text"
                  id="business_address"
                  name="business_address"
                  value={values.business_address}
                  onChange={handleChange}
                  placeholder="123 Business St., City"
                  className={`w-full px-4 py-3 rounded-lg border-0 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:bg-white ${
                    error?.business_address ? "ring-2 ring-red-500" : ""
                  }`}
                  required
                />
                {error?.business_address && (
                  <p className="text-red-500 text-sm mt-2">{error.business_address}</p>
                )}
              </div>

              {/* Business Contact */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-700 mb-3">
                  <Phone className="w-5 h-5 text-pink-500" />
                  Business Contact *
                </label>
                <input
                  type="text"
                  id="business_contact"
                  name="business_contact"
                  value={values.business_contact}
                  onChange={handleChange}
                  placeholder="09123456789"
                  className={`w-full px-4 py-3 rounded-lg border-0 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:bg-white ${
                    error?.business_contact ? "ring-2 ring-red-500" : ""
                  }`}
                  required
                />
                {error?.business_contact && (
                  <p className="text-red-500 text-sm mt-2">{error.business_contact}</p>
                )}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 py-4 bg-pink-500 text-white rounded-xl font-semibold hover:bg-pink-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-pink-500/30"
            >
              {isSubmitting ? "Submitting..." : "Submit Application"}
            </button>
            <button
              type="button"
              onClick={reset}
              className="px-8 py-4 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-colors"
            >
              Reset
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};