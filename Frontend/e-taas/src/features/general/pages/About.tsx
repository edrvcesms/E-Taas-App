import { Target, Users, Award, TrendingUp } from 'lucide-react';

export const About = () => {
  return (
    <div>
      {/* Header */}
      <section className="py-40 px-4 sm:px-6 lg:px-8 bg-linear-to-br from-pink-500/5 to-white">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-pink-500 mb-4">About E-TAAS ang Pinay MSMEs</h1>
          <p className="text-gray-700 max-w-xl mx-auto">
            Empowering Filipino women entrepreneurs through comprehensive training, mentoring, and digital marketing support.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-pink-500 mb-6">About the Program</h2>
            <p className="text-gray-700 leading-relaxed mb-4 text-justify">
              The E-TAAS ang Pinay MSMEs Program is a comprehensive training, mentoring, and promotion support program of DTI (Department of Trade and Industry) and NATCCO (National Confederation of Cooperatives) that aims to provide training and support on digital marketing for Filipino MSMEs, especially women entrepreneurs.
            </p>
            <p className="text-gray-700 leading-relaxed text-justify">
              This platform serves as the official e-commerce marketplace for E-TAAS members, providing them with a dedicated space to showcase and sell their products while receiving continuous support in their digital marketing journey.
            </p>
          </div>

          {/* Program Goals */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-pink-500 mb-8 text-center">Program Goals</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white rounded-2xl p-8 shadow-sm">
                <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mb-6">
                  <Target className="w-8 h-8 text-pink-500" />
                </div>
                <h3 className="text-xl font-semibold text-pink-500 mb-4">Goal 1: Training & Mentoring</h3>
                <p className="text-gray-700 leading-relaxed">
                  To train and mentor MSME entrepreneurs on digital marketing, equipping them with the skills and knowledge needed to succeed in the online marketplace and grow their businesses effectively.
                </p>
              </div>
              <div className="bg-white rounded-2xl p-8 shadow-sm">
                <div className="w-16 h-16 bg-pink-500/10 rounded-full flex items-center justify-center mb-6">
                  <TrendingUp className="w-8 h-8 text-pink-500" />
                </div>
                <h3 className="text-xl font-semibold text-pink-500 mb-4">Goal 2: Digital Marketing Support</h3>
                <p className="text-gray-700 leading-relaxed">
                  To provide ongoing support on digital marketing in partnership with social media and e-commerce platforms, ensuring MSMEs have the tools and resources to thrive online.
                </p>
              </div>
            </div>
          </div>

          {/* Partners */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-pink-500 mb-8 text-center">Our Partners</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-linear-to-br from-pink-500/5 to-white rounded-2xl p-8 text-center">
                <div className="w-24 h-24 bg-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                  <span className="text-white text-4xl font-bold">DTI</span>
                </div>
                <h3 className="text-xl font-semibold text-pink-500 mb-4">Department of Trade and Industry</h3>
                <p className="text-gray-700">
                  The primary government agency responsible for the development and promotion of Philippine industries and enterprises.
                </p>
              </div>
              <div className="bg-linear-to-br from-pink-500/5 to-white rounded-2xl p-8 text-center">
                <div className="w-24 h-24 bg-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                  <span className="text-white text-2xl font-bold">NATCCO</span>
                </div>
                <h3 className="text-xl font-semibold text-pink-500 mb-4">National Confederation of Cooperatives</h3>
                <p className="text-gray-700">
                  A network of cooperatives working together to promote cooperative development and empower Filipino entrepreneurs.
                </p>
              </div>
            </div>
          </div>

          {/* Key Features */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-pink-500 mb-8 text-center">What We Offer</h2>
            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-pink-500/10 rounded-full flex items-center justify-center shrink-0">
                  <Users className="w-6 h-6 text-pink-500" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-pink-500 mb-2">Dedicated E-Commerce Platform</h3>
                  <p className="text-gray-700">A marketplace exclusively for E-TAAS members to sell their products and reach customers nationwide.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-pink-500/10 rounded-full flex items-center justify-center shrink-0">
                  <Award className="w-6 h-6 text-pink-500" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-pink-500 mb-2">Comprehensive Training Programs</h3>
                  <p className="text-gray-700">From basic digital marketing to advanced e-commerce strategies, we provide training for all skill levels.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-pink-500/10 rounded-full flex items-center justify-center shrink-0">
                  <Target className="w-6 h-6 text-pink-500" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-pink-500 mb-2">One-on-One Mentoring</h3>
                  <p className="text-gray-700">Personalized guidance from experienced entrepreneurs and business coaches to help you grow.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-pink-500/10 rounded-full flex items-center justify-center shrink-0">
                  <TrendingUp className="w-6 h-6 text-pink-500" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-pink-500 mb-2">Digital Marketing Support</h3>
                  <p className="text-gray-700">Ongoing assistance with social media, content creation, and online promotional strategies.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Mission & Vision */}
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-linear-to-br from-pink-500/5 to-white rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-pink-500 mb-4">Our Mission</h3>
              <p className="text-gray-700 leading-relaxed">
                To empower Filipino women entrepreneurs and MSMEs by providing them with the knowledge, skills, and platform they need to succeed in the digital economy.
              </p>
            </div>
            <div className="bg-linear-to-br from-pink-500/5 to-white rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-pink-500 mb-4">Our Vision</h3>
              <p className="text-gray-700 leading-relaxed">
                A thriving community of digitally empowered Filipino MSMEs, particularly women entrepreneurs, competing successfully in the global marketplace.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-pink-500 mb-6">Join the E-TAAS Community</h2>
          <p className="text-gray-700 mb-8 leading-relaxed">
            Whether you're a customer looking to support local businesses or an entrepreneur wanting to grow your MSME, we're here to help you succeed.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button className="px-8 py-3 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity">
              Become a Seller
            </button>
            <button className="px-8 py-3 border-2 border-pink-500 text-pink-500 rounded-full hover:bg-pink-500/5 transition-colors">
              Shop Products
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}