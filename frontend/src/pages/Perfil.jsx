import { useEffect, useState } from "react";
import { getUserInfo } from "../services/api";
import { useNavigate } from "react-router-dom";

function Perfil() {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getUserInfo();
                setUser(res.data);
            } catch  {
                navigate("/login");
            }
        }
        load();
    }, []);

    if (!user) return <div className="container mt-4">Cargando...</div>;

    return (
        <div className="container mt-4">
            <h2>Mi Perfil</h2>

            <div className="card p-3 mt-3">
                <p><strong>Nombre:</strong> {user.nombre}</p>
                <p><strong>Correo:</strong> {user.correo}</p>
            </div>

            <button className="btn btn-primary mt-3" onClick={() => navigate("/editar-perfil")}>
                Editar Perfil
            </button>
        </div>
    );
}

export default Perfil;
