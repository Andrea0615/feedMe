import { useState } from "react";
import { loginUser } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

function Login() {
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const res = await loginUser({ correo, contrasena });
            localStorage.setItem("token", res.data.token);
            navigate("/home");
        } catch {
            alert("Credenciales inválidas");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>Iniciar Sesión</h2>
                    <p>Bienvenido a FeedMe</p>
                </div>

                <form onSubmit={handleSubmit}>
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
                        {loading ? "Cargando..." : "Entrar"}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>¿No tienes cuenta? <a href="/register">Regístrate aquí</a></p>
                </div>
            </div>
        </div>
    );
}

export default Login;
