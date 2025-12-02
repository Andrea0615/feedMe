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
            const res = await loginUser({
                correo,
                contrasena
            });

            localStorage.setItem("token", res.data.token);

            alert("Login correcto");
            navigate("/register-pet"); // redirigir al dashboard o a registrar mascota

        } catch (err) {
            console.log(err);
            alert("Credenciales inválidas");
        }
    };

    return (
        <div className="container mt-4">
            <h2>Iniciar Sesión</h2>

            <form onSubmit={handleSubmit} className="mt-3">
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

                <button className="btn btn-primary w-100">Entrar</button>
            </form>
        </div>
    );
}

export default Login;
