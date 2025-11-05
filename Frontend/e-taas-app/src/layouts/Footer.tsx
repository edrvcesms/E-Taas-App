
const Footer = () => {
  return (
    <>
      <footer className="bg-pink-500 text-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="mb-4">E-TAAS</h3>
            <p className="text-white/80 text-sm leading-relaxed">
              Empowering Filipino women entrepreneurs through digital marketing training and support.
            </p>
          </div>
          <div>
            <h4 className="mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#home" className="text-white/80 hover:text-white transition-colors">Home</a></li>
              <li><a href="#products" className="text-white/80 hover:text-white transition-colors">Products</a></li>
              <li><a href="#services" className="text-white/80 hover:text-white transition-colors">Services</a></li>
              <li><a href="#about" className="text-white/80 hover:text-white transition-colors">About Us</a></li>
            </ul>
          </div>
          <div>
            <h4 className="mb-4">Services</h4>
            <ul className="space-y-2 text-sm">
              <li className="text-white/80">Training</li>
              <li className="text-white/80">Mentoring</li>
              <li className="text-white/80">Digital Marketing</li>
              <li className="text-white/80">Platform Support</li>
            </ul>
          </div>
          <div>
            <h4 className="mb-4">Contact</h4>
            <ul className="space-y-2 text-sm">
              <li className="text-white/80">DTI Philippines</li>
              <li className="text-white/80">NATCCO</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-white/20 pt-8 text-center text-sm text-white/80">
          <p>© 2025 E-TAAS ang Pinay MSMEs. A program by DTI and NATCCO.</p>
        </div>
      </div>
    </footer>
    </>
  )
}

export default Footer