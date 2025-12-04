import { useEffect, useState } from "react";
import { getUserInfo } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/perfil.css";

function Perfil() {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getUserInfo();
                setUser(res.data);
            } catch {
                navigate("/login");
            }
        }
        load();
    }, []);

    if (!user) return <div className="container mt-4">Cargando...</div>;

    return (
        <div className="container mt-4 mb-4">
            <h2>Mi Perfil</h2>

            <div className="profile-card">
                <div className="profile-avatar">👤</div>
                <h3>{user.nombre}</h3>
                <p className="profile-email">{user.correo}</p>
            </div>

            <div className="card p-4 mb-4">
                <h5>Detalles</h5>
                <div className="profile-detail">
                    <span className="detail-label">👤 Nombre</span>
                    <span className="detail-value">{user.nombre}</span>
                </div>
                <div className="profile-detail">
                    <span className="detail-label">📧 Correo</span>
                    <span className="detail-value">{user.correo}</span>
                </div>
            </div>

            <button
                className="btn btn-primary btn-large w-100"
                onClick={() => navigate("/editar-perfil")}
            >
                ✎ Editar Perfil
            </button>
        </div>
    );
}

export default Perfil;
