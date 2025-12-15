import { Route, Routes } from "react-router-dom"
import './index.css'
import { useEffect } from "react"
import { Register } from "./features/auth/pages/Register"
import { VerifyOtp } from "./features/auth/pages/VerifyOtp"
import { useCurrentUser } from "./hooks/useCurrentUser"
import { Login } from "./features/auth/pages/Login"

function App() {

  return (
    <>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/verify-otp" element={<VerifyOtp />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </>
  )
}

export default App
