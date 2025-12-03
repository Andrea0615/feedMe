import { useEffect, useState } from "react";
import { getUserInfo, updateUserInfo } from "../services/api";
import { useNavigate } from "react-router-dom";

function EditarPerfil() {
    const [nombre, setNombre] = useState("");
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");

    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getUserInfo();
                setNombre(res.data.nombre);
                setCorreo(res.data.correo);
            } catch {
                navigate("/");
            }
        }
        load();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = { nombre, correo };
        if (contrasena.trim() !== "") payload.contrasena = contrasena;

        try {
            await updateUserInfo(payload);
            alert("Perfil actualizado");
            navigate("/ver-perfil");
        } catch {
            alert("Error al actualizar perfil");
        }
    };

    return (
        <div className="container mt-4">
            <h2>Editar Perfil</h2>

            <form onSubmit={handleSubmit}>
                <input className="form-control mb-2" value={nombre} onChange={(e) => setNombre(e.target.value)} />
                <input className="form-control mb-2" value={correo} onChange={(e) => setCorreo(e.target.value)} />
                <input className="form-control mb-2" type="password" placeholder="Nueva contraseña (opcional)" value={contrasena} onChange={(e) => setContrasena(e.target.value)} />
                <button className="btn btn-primary w-100 mt-3">Guardar cambios</button>
            </form>
        </div>
    );
}

export default EditarPerfil;
