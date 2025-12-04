import { useState } from "react";
import { loginUser } from "../services/api";
import { useNavigate } from "react-router-dom";

function Login() {
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await loginUser({ correo, contrasena });
            localStorage.setItem("token", res.data.token);

            navigate("/home");
        } catch {
            alert("Credenciales inválidas");
        }
    };

    return (
        <div className="container mt-4" style={{ maxWidth: "420px" }}>
            <h2 className="text-center mb-4">Iniciar Sesión</h2>

            <form
                onSubmit={handleSubmit}
                className="p-4 rounded"
                style={{ background: "white", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}
            >
                <input
                    className="form-control mb-3"
                    placeholder="Correo"
                    type="email"
                    value={correo}
                    onChange={(e) => setCorreo(e.target.value)}
                    required
                />

                <input
                    className="form-control mb-3"
                    placeholder="Contraseña"
                    type="password"
                    value={contrasena}
                    onChange={(e) => setContrasena(e.target.value)}
                    required
                />

                <button className="btn btn-primary w-100 py-2">Entrar</button>
            </form>
        </div>
    );
}

export default Login;
