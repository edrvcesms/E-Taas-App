import { Search, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { logoutUser } from '../services/user/UserDetails';
import { useNavigate } from 'react-router-dom';
import { client } from "../main";
import { useAuth } from '../context/AuthContext';
import etaasLogo from '../assets/etaaslogo.png';

const svgPaths = {
  p9e9700: "M8.73753 25.5405C10.0071 24.5697 11.426 23.8042 12.9943 23.2441C14.5626 22.684 16.2055 22.4039 17.9231 22.4039C19.6408 22.4039 21.2837 22.684 22.852 23.2441C24.4203 23.8042 25.8392 24.5697 27.1088 25.5405C27.98 24.5199 28.6584 23.3623 29.1438 22.0679C29.6292 20.7734 29.8719 19.3919 29.8719 17.9232C29.8719 14.6124 28.7082 11.7932 26.3806 9.46567C24.0531 7.13815 21.234 5.97439 17.9231 5.97439C14.6123 5.97439 11.7932 7.13815 9.46566 9.46567C7.13814 11.7932 5.97438 14.6124 5.97438 17.9232C5.97438 19.3919 6.21709 20.7734 6.70251 22.0679C7.18792 23.3623 7.86627 24.5199 8.73753 25.5405ZM17.9231 19.4168C16.4544 19.4168 15.216 18.9127 14.2078 17.9045C13.1997 16.8963 12.6956 15.6579 12.6956 14.1892C12.6956 12.7205 13.1997 11.482 14.2078 10.4738C15.216 9.46567 16.4544 8.96158 17.9231 8.96158C19.3919 8.96158 20.6303 9.46567 21.6385 10.4738C22.6466 11.482 23.1507 12.7205 23.1507 14.1892C23.1507 15.6579 22.6466 16.8963 21.6385 17.9045C20.6303 18.9127 19.3919 19.4168 17.9231 19.4168Z",
};

function AccountCircleIcon() {
  return (
    <svg className="w-9 h-9" fill="none" viewBox="0 0 36 36">
      <g>
        <mask height="36" id="mask0_1_7" maskUnits="userSpaceOnUse" style={{ maskType: "alpha" }} width="36" x="0" y="0">
          <rect fill="#D9D9D9" height="35.8463" width="35.8463" />
        </mask>
        <g mask="url(#mask0_1_7)">
          <path d={svgPaths.p9e9700} fill="white" />
        </g>
      </g>
    </svg>
  );
}

export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const { setIsAuthenticated, setUser } = useAuth();
  const navigate = useNavigate();

const handleLogout = async () => {
    try {
      await logoutUser();
      setIsAuthenticated(false);
      setUser(null);
      client.clear();
      navigate("/login");
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
            <img
              src={etaasLogo}
              alt="E-TAAS Logo"
              className="w-10 h-10 object-contain"
            />
            <div>
              <span className="text-pink-500 font-semibold text-lg">E-TAAS</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <a onClick={() => navigate("/")} className="text-pink-500 font-semibold hover:underline hover:cursor-pointer transition-opacity">HOME</a>
            <a onClick={() => navigate("/users/products")} className="text-pink-500 font-semibold hover:underline hover:cursor-pointer transition-opacity">PRODUCTS</a>
            <a onClick={() => navigate("/users/services")} className="text-pink-500 font-semibold hover:underline hover:cursor-pointer transition-opacity">SERVICES</a>
            <a onClick={() => navigate("/about")} className="text-pink-500 font-semibold hover:underline hover:cursor-pointer transition-opacity">ABOUT US</a>
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
              <button
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center hover:opacity-90 transition-opacity"
              >
                <AccountCircleIcon />
              </button>

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
