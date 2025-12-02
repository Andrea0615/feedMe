import { BrowserRouter, Routes, Route } from "react-router-dom";

// Páginas
import Register from "./pages/Register";
import Login from "./pages/Login";
import RegistrarMascota from "./pages/RegistrarMascota";
import Home from "./pages/Home";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/registrar-mascota" element={<RegistrarMascota />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
