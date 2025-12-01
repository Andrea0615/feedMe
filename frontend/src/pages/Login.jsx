import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function Login() {
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/auth/login", {
        correo,
        contrasena
      });

      localStorage.setItem("token", res.data.token);
      navigate("/dashboard");

    } catch {
      alert("Credenciales inválidas");
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "400px" }}>
      <h2>Iniciar sesión</h2>
      <form onSubmit={handleLogin}>
        
        <input
          className="form-control mb-2"
          type="email"
          placeholder="Correo"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
        />

        <input
          className="form-control mb-3"
          type="password"
          placeholder="Contraseña"
          value={contrasena}
          onChange={(e) => setContrasena(e.target.value)}
        />

        <button className="btn btn-success w-100">Entrar</button>
      </form>
    </div>
  );
}

export default Login;
