import { Route, Routes } from "react-router-dom"
import './index.css'
import { Home } from "./features/general/pages/Home"

function App() {

  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  )
}

export default App
