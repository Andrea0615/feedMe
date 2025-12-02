import { useState } from "react";
import { registerUser } from "../services/api";

function Register() {
    const [nombre, setNombre] = useState("");
    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await registerUser({
                nombre,
                correo,
                contrasena,
            });

            alert("Usuario registrado correctamente");
        } catch (err) {
            console.error(err);
            alert("Error al registrar usuario");
        }
    };

    return (
        <div className="container mt-4">
            <h2>Crear Cuenta</h2>

            <form onSubmit={handleSubmit} className="mt-3">
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
                    className="form-control mb-3"
                    placeholder="Contraseña"
                    type="password"
                    value={contrasena}
                    onChange={(e) => setContrasena(e.target.value)}
                    required
                />

                <button className="btn btn-primary w-100">Crear Cuenta</button>
            </form>
        </div>
    );
}

export default Register;
