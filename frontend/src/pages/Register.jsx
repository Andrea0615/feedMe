import { useState } from "react";
import { registerUser } from "../services/api";

function Register() {
    const [nombre, setNombre] = useState("");
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registerUser({ nombre, correo, contrasena });
            alert("Usuario registrado");
        } catch {
            alert("Error al registrar");
        }
    };

    return (
        <div className="container mt-4" style={{ maxWidth: "420px" }}>
            <h2 className="text-center mb-4">Crear Cuenta</h2>

            <form
                onSubmit={handleSubmit}
                className="p-4 rounded"
                style={{ background: "white", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}
            >
                <input
                    className="form-control mb-3"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />

                <input
                    className="form-control mb-3"
                    placeholder="Correo"
                    type="email"
                    value={correo}
                    onChange={(e) => setCorreo(e.target.value)}
                />

                <input
                    className="form-control mb-4"
                    placeholder="Contraseña"
                    type="password"
                    value={contrasena}
                    onChange={(e) => setContrasena(e.target.value)}
                />

                <button className="btn btn-primary w-100 py-2">Registrar</button>
            </form>
        </div>
    );
}

export default Register;
