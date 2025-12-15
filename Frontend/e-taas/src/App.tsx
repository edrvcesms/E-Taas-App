import { Route, Routes } from "react-router-dom"
import './index.css'
import { Register } from "./features/auth/pages/Register"
import { VerifyRegisterOtp } from "./features/auth/pages/VerifyRegisterOtp"
import { ForgotPassword } from "./features/auth/pages/ForgotPassword"
import { ResetPassword } from "./features/auth/pages/ResetPassword"
import { VerifyResetOtp } from "./features/auth/pages/VerifyPasswordOtp"
import { Login } from "./features/auth/pages/Login"

function App() {

  return (
    <>
      <Routes>
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
