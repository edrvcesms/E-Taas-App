import { Search, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { logoutUser } from '../services/user/UserDetails';
import { useNavigate } from 'react-router-dom';
import { queryClient } from '../main';
import { useCurrentUser } from '../store/currentUserStore';
import { User } from "lucide-react"


export function AccountCircleIcon() {
  return <User className="w-9 h-5 text-white font-bold" />;
}

export const LoginBtn = () => {
  const navigate = useNavigate();
  return (
    <button
      onClick={() => navigate("/login")}
      className="px-4 py-2 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity cursor-pointer"
    >
      Login
    </button>
  );
}

export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const currentUser = useCurrentUser((state) => state.currentUser);
  const [searchQuery, setSearchQuery] = useState('');
  const isLoading = useCurrentUser((state) => state.isLoading);
  const clearCurrentUser = useCurrentUser((state) => state.clearCurrentUser);
  const navigate = useNavigate();

const handleLogout = async () => {
    try {
      await logoutUser();
      clearCurrentUser();
      queryClient.clear();
      navigate("/login");
      setIsMenuOpen(false);
      setIsProfileOpen(false);
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center">
              <span className="text-white">E</span>
            </div>
            <span className="text-[#DD5BA3]">E-TAAS</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <a onClick={() => navigate("/")} className="text-pink-500 hover:underline hover:cursor-pointer transition-opacity">HOME</a>
            <a onClick={() => navigate("/products")} className="text-pink-500 hover:underline hover:cursor-pointer transition-opacity">PRODUCTS</a>
            <a onClick={() => navigate("/services")} className="text-pink-500 hover:underline hover:cursor-pointer transition-opacity">SERVICES</a>
            <a onClick={() => navigate("/about")} className="text-pink-500 hover:underline hover:cursor-pointer transition-opacity">ABOUT US</a>
          </div>

          {/* Search & Profile */}
          <div className="hidden lg:flex items-center gap-4 relative">
            <div className="relative">
              <input
                type="text"
                placeholder="Search Products ..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-80 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:border-[#DD5BA3] transition-colors"
              />
              <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>

            {/* Profile button */}
            <div className="relative">
              {currentUser ? (
                <button
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center hover:opacity-90 transition-opacity"
              >
                <AccountCircleIcon />
              </button>
              ) : (
                <LoginBtn />
              )}
              {/* Dropdown */}
              {isProfileOpen && (
                <div className="absolute right-0 mt-2 w-40 bg-white border border-gray-200 rounded-lg shadow-lg flex flex-col z-50">
                  <button
                    onClick={() => navigate("/profile")}
                    className="px-4 py-2 text-left hover:bg-gray-100 transition-colors"
                  >
                    Profile
                  </button>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 text-left hover:bg-gray-100 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-pink-500"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 space-y-4">
            <a onClick={() => navigate("/")} className="block text-pink-500 underline">HOME</a>
            <a onClick={() => navigate("/users/products")} className="block text-pink-500">PRODUCTS</a>
            <a onClick={() => navigate("/users/services")} className="block text-pink-500">SERVICES</a>
            <a onClick={() => navigate("/about")} className="block text-pink-500">ABOUT US</a>
            <div className="relative pt-2">
              <input
                type="text"
                placeholder="Search Products ..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:border-[#DD5BA3]"
              />
              <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};