import { Route, Routes } from "react-router-dom";
import "./index.css";
import { Register } from "./features/auth/pages/Register";
import { VerifyRegisterOtp } from "./features/auth/pages/VerifyRegisterOtp";
import { ForgotPassword } from "./features/auth/pages/ForgotPassword";
import { ResetPassword } from "./features/auth/pages/ResetPassword";
import { VerifyResetOtp } from "./features/auth/pages/VerifyPasswordOtp";
import { Login } from "./features/auth/pages/Login";
import { Home } from "./features/general/pages/Home";
import { About } from "./features/general/pages/About";
import { ProductsPage } from "./features/general/pages/Products";
import { Profile } from "./features/user/pages/Profile";
import { LoadingIndicator } from "./features/general/components/LoadingIndicator";
import Services from "./features/general/pages/Services";
import { MyContextProvider } from "./context/MyContext";
import { useCurrentUser } from "./store/currentUserStore";
import { useEffect } from "react";
import { UserProtectedRoutes } from "./routes/UserProtectedRoutes";
import { AuthLayout } from "./layouts/AuthLayout";
import { Navbar } from "./layouts/Navbar";
import Footer from "./layouts/Footer";
import ProductDetails from "./features/general/pages/ProductDetails";

function App() {
  const isLoading = useCurrentUser((state) => state.isLoading);
  const checkStoredUser = useCurrentUser((state) => state.checkStoredUser);

  useEffect(() => {
    checkStoredUser();
  }, [checkStoredUser]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingIndicator size={60} />
      </div>
    );
  }

  return (
    <MyContextProvider>
      <Navbar />
      <Routes>
        <Route element={<UserProtectedRoutes />}>
          <Route path="/profile" element={<Profile />} />
        </Route>

        <Route path="/" element={<Home />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/products/:productId" element={<ProductDetails />} />
        <Route path="/services" element={<Services />} />
        <Route path="/about" element={<About />} />

        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-register-otp" element={<VerifyRegisterOtp />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/verify-reset-otp" element={<VerifyResetOtp />} />
        </Route>
      </Routes>
      <Footer />
    </MyContextProvider>
  );
}

export default App;