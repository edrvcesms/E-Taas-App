import { useState } from 'react';
import { ShoppingCart, Star } from 'lucide-react';

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  seller: string;
  rating: number;
  image: string;
  description: string;
}

const mockProducts: Product[] = [
  {
    id: 1,
    name: "Homemade Strawberry Jam",
    category: "Jams",
    price: 250,
    seller: "Maria's Kitchen",
    rating: 4.8,
    image: "https://preppykitchen.com/wp-content/uploads/2021/08/Strawberry-Jam-RECIPE.jpg",
    description: "Authentic homemade strawberry jam with natural ingredients"
  },
  {
    id: 2,
    name: "Organic Mango Jam",
    category: "Jams",
    price: 280,
    seller: "Sweet Harvest",
    rating: 4.9,
    image: "https://mirchi.com/os/cdn/content/images/organic%20mango%20jam%20with%20fruit%20pieces%20himsrot_medium_0813352.webp",
    description: "Fresh organic mango jam from Guimaras"
  },
  {
    id: 3,
    name: "Premium Cashew Nuts",
    category: "Nuts",
    price: 450,
    seller: "Nutty Delights",
    rating: 4.7,
    image: "https://img.lazcdn.com/g/ff/kf/Sb25c0ceb5a9e414e80ea9571e421aa58R.jpg_720x720q80.jpg_.webp",
    description: "Roasted and salted premium cashew nuts"
  },
  {
    id: 4,
    name: "Mixed Nuts Pack",
    category: "Nuts",
    price: 380,
    seller: "Healthy Bites",
    rating: 4.6,
    image: "https://static-01.daraz.lk/p/456493ae67d399063bee23864f26a519.jpg",
    description: "Assorted roasted nuts - perfect for snacking"
  },
  {
    id: 5,
    name: "Coconut Vinegar",
    category: "Vinegar",
    price: 120,
    seller: "Pinoy Essentials",
    rating: 4.9,
    image: "https://www.organics.ph/cdn/shop/products/bibliorganics-coconut-cider-vinegar-750ml-pantry-bibliorganics-816713_1024x.jpg?v=1657894353",
    description: "Traditional Filipino coconut vinegar"
  },
  {
    id: 6,
    name: "Pineapple Vinegar",
    category: "Vinegar",
    price: 150,
    seller: "Farm Fresh",
    rating: 4.8,
    image: "https://i.pinimg.com/736x/59/f3/7c/59f37c712e9f402e0f1b31da761ec1c9.jpg",
    description: "Sweet and tangy pineapple vinegar"
  },
  {
    id: 7,
    name: "Fresh Tomatoes",
    category: "Vegetables",
    price: 80,
    seller: "Green Valley Farm",
    rating: 4.5,
    image: "https://foodal.com/wp-content/uploads/2016/08/three-tomatoes.jpg",
    description: "Farm-fresh organic tomatoes per kilo"
  },
  {
    id: 8,
    name: "Organic Lettuce",
    category: "Vegetables",
    price: 60,
    seller: "Healthy Greens",
    rating: 4.7,
    image: "https://farmlinkhawaii.com/cdn/shop/files/Organic_20green_20leaf_20lettuce-800x533.jpg?v=1724304975",
    description: "Crisp organic lettuce, hydroponically grown"
  },
  {
    id: 9,
    name: "Mixed Vegetables Pack",
    category: "Vegetables",
    price: 200,
    seller: "Fresh Harvest",
    rating: 4.6,
    image: "https://5.imimg.com/data5/ANDROID/Default/2023/2/JK/EI/NT/38389593/product-jpeg.jpg",
    description: "Assorted fresh vegetables from local farms"
  },
  {
    id: 10,
    name: "Organic Honey",
    category: "Honey",
    price: 350,
    seller: "Bee Natural",
    rating: 4.9,
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRB191_zstT2S0oaqTGu4UuQgxOqy4a7JqntA&s",
    description: "Pure organic honey from local bees"
  }
];



const categories = ["All", "Jams", "Nuts", "Vinegar", "Vegetables"];

export const Products = () => {
  const [selectedCategory, setSelectedCategory] = useState("All");

  const filteredProducts = selectedCategory === "All" 
    ? mockProducts 
    : mockProducts.filter(p => p.category === selectedCategory);

  return (
    <div>
      {/* Header */}
  <section className="py-12 px-4 sm:px-6 lg:px-8 bg-linear-to-br from-pink-500/5 to-white">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-pink-500 mb-4">Our Products</h1>
          <p className="text-gray-700 max-w-3xl">
            Browse quality products from verified E-TAAS members. Every purchase supports Filipino women entrepreneurs.
          </p>
        </div>
      </section>

      {/* Category Filter */}
      <section className="py-8 px-4 sm:px-6 lg:px-8 border-b border-gray-200">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-wrap gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-full transition-colors ${
                  selectedCategory === category
                    ? 'bg-[#DD5BA3] text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredProducts.map((product) => (
              <div key={product.id} className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-shadow">
                <div className="w-full h-64 bg-gray-100 overflow-hidden">
  <img
    src={product.image}
    alt={product.name}
    className="w-full h-full object-cover"
  />
</div>
                <div className="p-6">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h3 className="text-pink-500 mb-1">{product.name}</h3>
                      <p className="text-sm text-gray-600">{product.seller}</p>
                    </div>
                    <span className="bg-pink-500/10 text-pink-500 px-3 py-1 rounded-full text-sm">
                      {product.category}
                    </span>
                  </div>
                  <p className="text-gray-700 text-sm mb-4 line-clamp-2">{product.description}</p>
                  <div className="flex items-center gap-1 mb-4">
                    <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm text-gray-700">{product.rating}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-pink-500">₱{product.price}</span>
                    <button className="px-4 py-2 bg-pink-500 text-white rounded-full hover:opacity-90 transition-opacity flex items-center gap-2">
                      <ShoppingCart className="w-4 h-4" />
                      Add to Cart
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
