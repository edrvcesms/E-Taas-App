import { useEffect } from "react";
import { motion } from "framer-motion";
import { useAuth } from "../../context/AuthContext";
import { logoutUser } from "../../services/user/UserDetails";
import Footer from "../../layouts/Footer";
import { useNavigate } from "react-router-dom";
import { client } from "../../main";
import { ShoppingBag, Users, TrendingUp, Award } from 'lucide-react';
import image from "../../assets/image.png"

// Animation variants - All bottom to top
const fadeInUp = {
  hidden: { opacity: 0, y: 60 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.7, ease: "easeOut" }
  }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
      delayChildren: 0.1
    }
  }
};

const Home: React.FC = () => {
  const { isAuthenticated, setIsAuthenticated, setUser, isLoading, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isLoading) return; 
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, isLoading, navigate]);

  if (!isAuthenticated) return null;

  return (
    <div>
      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-[#DD5BA3]/5 to-white overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, amount: 0.3 }}
              variants={staggerContainer}
            >
              <motion.h1 
                className="text-pink-500 mb-6 font-semibold text-5xl"
                variants={fadeInUp}
              >
                Your Trusted Marketplace for Filipino MSMEs
              </motion.h1>
              <motion.p 
                className="text-gray-700 leading-relaxed mb-8"
                variants={fadeInUp}
              >
                Welcome to the E-TAAS Marketplace - a dedicated e-commerce platform connecting Filipino women entrepreneurs and small business owners with customers nationwide. Discover quality products from verified E-TAAS members and support local businesses.
              </motion.p>
              <motion.div 
                className="flex flex-wrap gap-4"
                variants={fadeInUp}
              >
                <motion.button 
                  onClick={() => navigate('/users/products')}
                  className="px-8 py-3 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Shop Now
                </motion.button>
                <motion.button 
                  onClick={() => navigate('/about')}
                  className="px-8 py-3 border-2 border-pink-500 text-pink-500 rounded-full hover:bg-pink-500/5 transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Learn More
                </motion.button>
              </motion.div>
            </motion.div>
            <motion.div 
              className="relative"
              initial={{ opacity: 0, y: 60 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <div className="bg-white shadow-md rounded-3xl flex items-center justify-center p-6">
                <div className="text-center">
                  <img
                    src={image}
                    alt="Marketplace Illustration"
                    className="w-full h-full object-contain"
                  />
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="grid md:grid-cols-4 gap-8"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={staggerContainer}
          >
            {[
              { icon: Users, number: "500+", label: "Active Sellers" },
              { icon: ShoppingBag, number: "2,000+", label: "Products" },
              { icon: TrendingUp, number: "95%", label: "Satisfaction Rate" },
              { icon: Award, number: "100%", label: "Verified Sellers" }
            ].map((stat, index) => (
              <motion.div 
                key={index}
                className="text-center"
                variants={fadeInUp}
                whileHover={{ y: -5, transition: { duration: 0.2 } }}
              >
                <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <stat.icon className="w-8 h-8 text-pink-500" />
                </div>
                <div className="text-pink-500 mb-2 text-3xl font-bold">
                  {stat.number}
                </div>
                <p className="text-gray-600">{stat.label}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <motion.h2 
            className="text-center text-pink-500 mb-12 text-2xl"
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.5 }}
            transition={{ duration: 0.6 }}
          >
            Why Shop With Us?
          </motion.h2>
          <motion.div 
            className="grid md:grid-cols-3 gap-8"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={staggerContainer}
          >
            {[
              { emoji: "✓", title: "Verified Sellers", description: "All sellers are verified E-TAAS members, ensuring quality and reliability in every transaction." },
              { emoji: "🇵🇭", title: "Support Local", description: "Every purchase directly supports Filipino women entrepreneurs and their families." },
              { emoji: "⭐", title: "Quality Products", description: "Handpicked products from skilled artisans and entrepreneurs across the Philippines." }
            ].map((feature, index) => (
              <motion.div 
                key={index}
                className="bg-white rounded-2xl p-8 text-center hover:shadow-lg transition-shadow"
                variants={fadeInUp}
                whileHover={{ 
                  y: -10,
                  transition: { duration: 0.3 }
                }}
              >
                <motion.div 
                  className="w-20 h-20 bg-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center"
                  whileHover={{ 
                    rotate: [0, -10, 10, -10, 0],
                    transition: { duration: 0.5 }
                  }}
                >
                  <span className="text-white text-3xl">{feature.emoji}</span>
                </motion.div>
                <h3 className="text-pink-500 mb-4 text-xl font-semibold">{feature.title}</h3>
                <p className="text-gray-700">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <motion.div 
          className="max-w-4xl mx-auto text-center"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.5 }}
          variants={staggerContainer}
        >
          <motion.h2 
            className="text-pink-500 mb-6 text-2xl"
            variants={fadeInUp}
          >
            Ready to Get Started?
          </motion.h2>
          <motion.p 
            className="text-gray-700 mb-8 leading-relaxed"
            variants={fadeInUp}
          >
            Join thousands of satisfied customers supporting Filipino MSMEs. Browse our marketplace and discover amazing products today!
          </motion.p>
          <motion.button 
            onClick={() => navigate('/users/products')}
            className="px-10 py-4 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity"
            variants={fadeInUp}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Explore Products
          </motion.button>
        </motion.div>
      </section>
    </div>
  );
};

export default Home;