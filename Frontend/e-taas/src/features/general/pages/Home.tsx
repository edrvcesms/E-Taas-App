import { useNavigate } from "react-router-dom";
import { Award, ShoppingBag, TrendingUp, Users } from "lucide-react";
import React from "react";



export const Home: React.FC = () => {
  const navigate = useNavigate();
  const etaasLogo = "/assets/etaas-marketplace-illustration.png";

return (
    <div>
      {/* Hero Section */}
      <section className="py-40 px-4 sm:px-6 lg:px-8 bg-linear-to-br from-pink-500/5 to-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl font-bold text-pink-500 mb-6">Your Trusted Marketplace for Filipino MSMEs</h1>
              <p className="text-gray-700 leading-relaxed mb-8">
                Welcome to the E-TAAS Marketplace - a dedicated e-commerce platform connecting Filipino women entrepreneurs and small business owners with customers nationwide. Discover quality products from verified E-TAAS members and support local businesses.
              </p>
              <div className="flex flex-wrap gap-4">
                <button 
                  onClick={() => navigate('/users/products')}
                  className="px-8 py-3 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity"
                >
                  Shop Now
                </button>
                <button 
                  onClick={() => navigate('/about')}
                  className="px-8 py-3 border-2 border-pink-500 text-pink-500 rounded-full hover:bg-pink-500/5 transition-colors"
                >
                  Learn More
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white shadow-md rounded-3xl p-12 aspect-square flex items-center justify-center">
                <div className="text-center">
                  <img
                    src={etaasLogo}
                    alt="Marketplace Illustration"
                    className="w-full h-auto max-w-md mx-auto"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-pink-500" />
              </div>
              <div className="text-3xl font-bold text-pink-500 mb-2">500+</div>
              <p className="text-gray-600">Active Sellers</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <ShoppingBag className="w-8 h-8 text-pink-500" />
              </div>
              <div className="text-3xl font-bold text-pink-500 mb-2">2,000+</div>
              <p className="text-gray-600">Products</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8 text-pink-500" />
              </div>
              <div className="text-3xl font-bold text-pink-500 mb-2">95%</div>
              <p className="text-gray-600">Satisfaction Rate</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="w-8 h-8 text-pink-500" />
              </div>
              <div className="text-3xl font-bold text-pink-500 mb-2">100%</div>
              <p className="text-gray-600">Verified Sellers</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-pink-500 mb-12">Why Shop With Us?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-20 h-20 bg-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-white text-3xl">✓</span>
              </div>
              <h3 className="text-xl font-semibold text-pink-500 mb-4">Verified Sellers</h3>
              <p className="text-gray-700">All sellers are verified E-TAAS members, ensuring quality and reliability in every transaction.</p>
            </div>
            <div className="bg-white rounded-2xl p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-20 h-20 bg-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-white text-3xl">🇵🇭</span>
              </div>
              <h3 className="text-xl font-semibold text-pink-500 mb-4">Support Local</h3>
              <p className="text-gray-700">Every purchase directly supports Filipino women entrepreneurs and their families.</p>
            </div>
            <div className="bg-white rounded-2xl p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-20 h-20 bg-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-white text-3xl">⭐</span>
              </div>
              <h3 className="text-xl font-semibold text-pink-500 mb-4">Quality Products</h3>
              <p className="text-gray-700">Handpicked products from skilled artisans and entrepreneurs across the Philippines.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-pink-500 mb-6">Ready to Get Started?</h2>
          <p className="text-gray-700 mb-8 leading-relaxed">
            Join thousands of satisfied customers supporting Filipino MSMEs. Browse our marketplace and discover amazing products today!
          </p>
          <button 
            onClick={() => navigate('/products')}
            className="px-10 py-4 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity text-lg font-semibold"
          >
            Explore Products
          </button>
        </div>
      </section>
    </div>
  );
};

export default Home;