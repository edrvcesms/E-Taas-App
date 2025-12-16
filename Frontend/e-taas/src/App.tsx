import { Route, Routes, useNavigate } from "react-router-dom"
import './index.css'
import { Register } from "./features/auth/pages/Register"
import { VerifyRegisterOtp } from "./features/auth/pages/VerifyRegisterOtp"
import { ForgotPassword } from "./features/auth/pages/ForgotPassword"
import { ResetPassword } from "./features/auth/pages/ResetPassword"
import { VerifyResetOtp } from "./features/auth/pages/VerifyPasswordOtp"
import { Login } from "./features/auth/pages/Login"
import { useCurrentUser } from "./hooks/useCurrentUser"
import { useEffect } from "react"
import { Home } from "./features/general/pages/Home"
import { refreshToken } from "./services/auth/Token"

function App() {

  const navigate = useNavigate();

  const { currentUser, checkStoredUser } = useCurrentUser();

  useEffect(() => {
    const isAuthenticated = async () => {
      await checkStoredUser();
      const storedUser = localStorage.getItem("currentUser");
      if (!storedUser) {
        try {
          await refreshToken();
          await checkStoredUser();
        } catch {
          console.log("No valid session found");
        }
      }
    };
    isAuthenticated();
  }, [checkStoredUser, navigate]);

  useEffect(() => {
  if (currentUser === null) navigate("/login");
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
