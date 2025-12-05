import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import BottomNav from "./components/BottomNav";
import PrivateRoute from "./components/PrivateRoute";


// Páginas
import Register from "./pages/Register";
import Login from "./pages/Login";
import RegistrarMascota from "./pages/RegistrarMascota";
import Home from "./pages/Home";
import MascotaInfo from "./pages/MascotaInfo"
import EditMascota from "./pages/EditMascota";
import Perfil from "./pages/Perfil";
import EditarPerfil from "./pages/EditarPerfil";
import EditarHorarios from "./pages/EditarHorarios";
import CamaraMascota from "./pages/CamaraMascota";
import EventosHistorial from "./pages/EventosHistorial";


function App() {
    return (
        <BrowserRouter>
            <Navbar />
            <Routes>
                <Route path="/" element={<PrivateRoute> <Home /> </PrivateRoute>} />
                <Route path="/home" element={<PrivateRoute> <Home /> </PrivateRoute>} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/registrar-mascota" element={<PrivateRoute> <RegistrarMascota /> </PrivateRoute>} />
                <Route path="/ver-mascota" element={<PrivateRoute> <MascotaInfo /> </PrivateRoute>} />
                <Route path="/editar-mascota" element={<PrivateRoute> <EditMascota /> </PrivateRoute>} />
                <Route path="/ver-perfil" element={<PrivateRoute> <Perfil /> </PrivateRoute>} />
                <Route path="/editar-perfil" element={<PrivateRoute> <EditarPerfil /> </PrivateRoute>} />
                <Route path="/horarios/editar" element={<PrivateRoute> <EditarHorarios /> </PrivateRoute>} />
                <Route path="/ver-camara" element={<CamaraMascota />} />
                <Route path="/mascota" element={<CamaraMascota />} />
                <Route path="/eventos" element={<EventosHistorial.jsx />} />
            </Routes>
            <BottomNav />
        </BrowserRouter>
    );
}

export default App;
