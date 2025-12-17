import { Route, Routes, useNavigate } from "react-router-dom"
import './index.css'
import { Register } from "./features/auth/pages/Register"
import { VerifyRegisterOtp } from "./features/auth/pages/VerifyRegisterOtp"
import { ForgotPassword } from "./features/auth/pages/ForgotPassword"
import { ResetPassword } from "./features/auth/pages/ResetPassword"
import { VerifyResetOtp } from "./features/auth/pages/VerifyPasswordOtp"
import { Login } from "./features/auth/pages/Login"
import { useCurrentUser } from "./store/currentUserStore"
import { useEffect } from "react"
import { Home } from "./features/general/pages/Home"

function App() {

  const navigate = useNavigate();

  const currentUser = useCurrentUser((state) => state.currentUser);
  const checkUser = useCurrentUser((state) => state.checkStoredUser);


  useEffect(() => {
    const initializeAuth = async () => {
      checkUser();
    }
    initializeAuth();
  }, []);

  useEffect(() => {
    if (currentUser) {
      navigate("/");
    } else {
      navigate("/login");
    }
  }, [currentUser, navigate]);
  

  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/verify-otp" element={<VerifyRegisterOtp />} />
        <Route path="/reset-password-verify-otp" element={<VerifyResetOtp />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </>
  )
}

export default App
