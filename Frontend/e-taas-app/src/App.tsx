import './App.css'
import { Routes, Route } from 'react-router-dom'
import Register from './pages/user/auth/Register'
import Login from './pages/user/auth/Login'
import { AuthProvider, useAuth } from './context/AuthContext'
import Home from './pages/user/Home'
import { UserProtectedRoutes } from './routes/UserProtectedRoutes'
import UserPage from './pages/user/UserPage'
import { Navbar } from './layouts/Navbar'
import { Products } from './pages/user/user/Products'
import { Services } from './pages/user/user/Services'
import { About } from './pages/user/About'
import Footer from './layouts/Footer'

function App() {

  return (
    <>
      <AuthProvider>
        <Main />

      </AuthProvider>
    </>
  )
}

const Main: React.FC = () => {
  
  const { isAuthenticated } = useAuth();
  return (
    <>
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        <Route path="/users" element={
          <UserProtectedRoutes>
            <UserPage />
          </UserProtectedRoutes>
        }>
          <Route path="products" element={<Products />} />
          <Route path="services" element={<Services />} />
        </Route>
      </Routes>
      {isAuthenticated && <Footer />}
    </>
  );
}

export default App


