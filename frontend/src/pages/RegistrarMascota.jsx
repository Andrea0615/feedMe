import { useState } from "react";
import { registrarMascota } from "../services/api";

function RegistrarMascota() {
    // Datos de la mascota
    const [nombre, setNombre] = useState("");
    const [edad, setEdad] = useState("");
    const [peso, setPeso] = useState("");

    // Plan alimenticio
    const [comidasPorDia, setComidasPorDia] = useState(1);

    // Horarios dinámicos
    const [horarios, setHorarios] = useState([{ hora: "", porcion: "" }]);

    const agregarHorario = () => {
        setHorarios([...horarios, { hora: "", porcion: "" }]);
    };

    const actualizarHorario = (index, campo, valor) => {
        const copia = [...horarios];
        copia[index][campo] = valor;
        setHorarios(copia);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = {
            mascota: {
                nombre,
                edad: Number(edad),
                peso: Number(peso)
            },
            alimentacion: {
                comidas_por_dia: Number(comidasPorDia),
                horarios: horarios.map(h => ({
                    hora: h.hora,
                    porcion: Number(h.porcion)
                }))
            }
        };

        try {
            await registrarMascota(payload);
            alert("Mascota registrada correctamente");
        } catch (err) {
            console.error(err);
            alert("Error al registrar mascota");
        }
    };

    return (
        <div className="container mt-4">
            <h2>Registrar Mascota</h2>

            <form onSubmit={handleSubmit} className="mt-3">

                {/* Datos de la mascota */}
                <div className="card p-3 mb-4">
                    <h5>Información de la mascota</h5>

                    <input
                        className="form-control mb-2"
                        placeholder="Nombre"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />

                    <input
                        className="form-control mb-2"
                        placeholder="Edad"
                        type="number"
                        value={edad}
                        onChange={(e) => setEdad(e.target.value)}
                    />

                    <input
                        className="form-control mb-2"
                        placeholder="Peso (kg)"
                        type="number"
                        value={peso}
                        onChange={(e) => setPeso(e.target.value)}
                    />
                </div>

                {/* Plan alimenticio */}
                <div className="card p-3 mb-4">
                    <h5>Plan Alimenticio</h5>

                    <input
                        className="form-control mb-2"
                        placeholder="Comidas por día"
                        type="number"
                        value={comidasPorDia}
                        onChange={(e) => setComidasPorDia(e.target.value)}
                        required
                    />

                    <h6 className="mt-3">Horarios</h6>

                    {horarios.map((h, index) => (
                        <div key={index} className="d-flex gap-2 mb-2">
                            <input
                                type="time"
                                className="form-control"
                                value={h.hora}
                                onChange={(e) => actualizarHorario(index, "hora", e.target.value)}
                                required
                            />

                            <input
                                className="form-control"
                                placeholder="Porción (g)"
                                type="number"
                                value={h.porcion}
                                onChange={(e) => actualizarHorario(index, "porcion", e.target.value)}
                                required
                            />
                        </div>
                    ))}

                    <button type="button" className="btn btn-secondary mt-2" onClick={agregarHorario}>
                        + Agregar horario
                    </button>
                </div>

                <button className="btn btn-primary w-100">Registrar</button>
            </form>
        </div>
    );
}

export default RegistrarMascota;
