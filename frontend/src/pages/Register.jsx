import { useState } from "react";
import { registerUser } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

function Register() {
    const [nombre, setNombre] = useState("");
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            await registerUser({ nombre, correo, contrasena });
            alert("Usuario registrado");
            navigate("/login");
        } catch {
            alert("Error al registrar");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>Crear Cuenta</h2>
                    <p>Únete a FeedMe</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <input
                        className="form-control mb-3"
                        placeholder="Nombre"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />

                    <input
                        className="form-control mb-3"
                        placeholder="Correo"
                        type="email"
                        value={correo}
                        onChange={(e) => setCorreo(e.target.value)}
                        required
                    />

                    <input
                        className="form-control mb-4"
                        placeholder="Contraseña"
                        type="password"
                        value={contrasena}
                        onChange={(e) => setContrasena(e.target.value)}
                        required
                    />

                    <button className="btn btn-primary w-100" disabled={loading}>
                        {loading ? "Registrando..." : "Registrar"}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>¿Ya tienes cuenta? <a href="/login">Inicia sesión</a></p>
                </div>
            </div>
        </div>
    );
}

export default Register;
