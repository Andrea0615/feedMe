import { useEffect, useState } from "react";
import { getUserInfo, updateUserInfo } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/editar-perfil.css";

function EditarPerfil() {
    const [nombre, setNombre] = useState("");
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getUserInfo();
                setNombre(res.data.nombre);
                setCorreo(res.data.correo);
            } catch (err) {
                console.log("Error cargando perfil:", err);
                navigate("/");
            }
        }
        load();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const payload = { 
                nombre, 
                correo 
            };
            if (contrasena.trim() !== "") {
                payload.contrasena = contrasena;
            }

            console.log("Enviando payload:", payload);
            const res = await updateUserInfo(payload);
            console.log("Respuesta:", res);
            
            alert("Perfil actualizado ✅");
            navigate("/ver-perfil");
        } catch (err) {
            console.log("Error completo:", err);
            alert("Error al actualizar perfil: " + (err.response?.data?.msg || err.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4 mb-4">
            <h2>Editar Perfil</h2>

            <form className="card p-4" onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Nombre</label>
                    <input
                        className="form-control"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />
                </div>

                <div className="mb-3">
                    <label className="form-label">Correo</label>
                    <input
                        className="form-control"
                        type="email"
                        value={correo}
                        onChange={(e) => setCorreo(e.target.value)}
                        required
                    />
                </div>

                <div className="mb-4">
                    <label className="form-label">Nueva contraseña (opcional)</label>
                    <input
                        className="form-control"
                        type="password"
                        placeholder="Dejar en blanco para no cambiar"
                        value={contrasena}
                        onChange={(e) => setContrasena(e.target.value)}
                    />
                </div>

                <button className="btn btn-primary btn-large w-100" disabled={loading}>
                    {loading ? "Guardando..." : "Guardar cambios"}
                </button>
            </form>
        </div>
    );
}

export default EditarPerfil;