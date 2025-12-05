import { useState } from "react";
import { registrarMascota } from "../services/api";
import { useNavigate } from "react-router-dom";

function RegistrarMascota() {
    const [nombre, setNombre] = useState("");
    const [edad, setEdad] = useState("");
    const [peso, setPeso] = useState("");
    const [objetivo, setObjetivo] = useState("");
    const [comidasPorDia, setComidasPorDia] = useState(1);
    const [horarios, setHorarios] = useState([{ hora: "", porcion: "" }]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const objetivos = [
        "Mantener peso",
        "Bajar de peso",
        "Subir de peso",
        "Cachorro activo",
        "Adulto mayor"
    ];

    const agregarHorario = () => {
        setHorarios([...horarios, { hora: "", porcion: "" }]);
    };

    const actualizarHorario = (index, campo, valor) => {
        const copia = [...horarios];
        copia[index][campo] = valor;
        setHorarios(copia);
    };

    const eliminarHorario = (index) => {
        setHorarios(horarios.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const payload = {
            mascota: {
                nombre,
                edad: Number(edad),
                peso: Number(peso),
                objetivo
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
            navigate("/home");
        } catch (err) {
            console.error(err);
            alert("Error al registrar mascota");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4 mb-4">
            <h2>Registrar Mascota</h2>

            <form onSubmit={handleSubmit}>
                <div className="card p-4 mb-4">
                    <h5>Información de la mascota</h5>

                    <div className="mb-3">
                        <label className="form-label">Nombre</label>
                        <input
                            className="form-control"
                            placeholder="Ej: Max"
                            value={nombre}
                            onChange={(e) => setNombre(e.target.value)}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Edad (años)</label>
                        <input
                            className="form-control"
                            type="number"
                            value={edad}
                            onChange={(e) => setEdad(e.target.value)}
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Peso (kg)</label>
                        <input
                            className="form-control"
                            type="number"
                            step="0.1"
                            value={peso}
                            onChange={(e) => setPeso(e.target.value)}
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Objetivo de salud</label>
                        <select
                            className="form-control"
                            value={objetivo}
                            onChange={(e) => setObjetivo(e.target.value)}
                            required
                        >
                            <option value="">Selecciona un objetivo</option>
                            {objetivos.map((obj) => (
                                <option key={obj} value={obj}>
                                    {obj}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="card p-4 mb-4">
                    <h5>Plan Alimenticio</h5>

                    <div className="mb-3">
                        <label className="form-label">Comidas por día</label>
                        <input
                            className="form-control"
                            type="number"
                            min="1"
                            value={comidasPorDia}
                            onChange={(e) => setComidasPorDia(e.target.value)}
                            required
                        />
                    </div>

                    <h6 className="mb-3">Horarios</h6>

                    <div className="mb-3">
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
                                    placeholder="g"
                                    type="number"
                                    value={h.porcion}
                                    onChange={(e) => actualizarHorario(index, "porcion", e.target.value)}
                                    required
                                />
                                {horarios.length > 1 && (
                                    <button
                                        type="button"
                                        className="btn btn-danger"
                                        onClick={() => eliminarHorario(index)}
                                        style={{ width: "48px", padding: "0" }}
                                    >
                                        X
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>

                    <button
                        type="button"
                        className="btn btn-secondary w-100 mb-3"
                        onClick={agregarHorario}
                    >
                        + Agregar horario
                    </button>
                </div>

                <div className="d-flex flex-column gap-2 mb-4">
                    <button className="btn btn-primary" disabled={loading}>
                        {loading ? "Registrando..." : "Registrar"}
                    </button>
                    <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => navigate("/home")}
                    >
                        Cancelar
                    </button>
                </div>
            </form>
        </div>
    );
}

export default RegistrarMascota;
