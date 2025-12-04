import { useEffect, useState } from "react";
import { getMascotaInfo, updateHorarios } from "../services/api";
import { useNavigate } from "react-router-dom";

function EditarHorarios() {
    const [horarios, setHorarios] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        getMascotaInfo()
            .then(res => setHorarios(res.data.horarios))
            .catch(() => alert("Error al cargar horarios"));
    }, []);

    const cambiarHorario = (index, campo, valor) => {
        const copia = [...horarios];
        copia[index][campo] = valor;
        setHorarios(copia);
    };

    const agregarHorario = () => {
        setHorarios([...horarios, { hora: "", porcion: "" }]);
    };

    const eliminarHorario = (index) => {
        const copia = horarios.filter((_, i) => i !== index);
        setHorarios(copia);
    };

    const guardarCambios = async () => {
        if (horarios.length === 0) {
            alert("Debes tener al menos un horario");
            return;
        }

        setLoading(true);

        try {
            await updateHorarios(
                horarios.map(h => ({
                    hora: h.hora,
                    porcion: Number(h.porcion),
                }))
            );

            alert("Horarios actualizados");
            navigate("/home");
        } catch (err) {
            alert("Error al guardar horarios");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4 mb-4">
            <h2>Editar Horarios</h2>

            <div className="card p-4 mb-4">
                <div className="mb-3">
                    {horarios.map((h, index) => (
                        <div key={index} className="d-flex gap-2 mb-2">
                            <input
                                type="time"
                                className="form-control"
                                value={h.hora}
                                onChange={(e) => cambiarHorario(index, "hora", e.target.value)}
                                required
                            />

                            <input
                                type="number"
                                placeholder="Porción (g)"
                                className="form-control"
                                value={h.porcion}
                                onChange={(e) => cambiarHorario(index, "porcion", e.target.value)}
                                required
                            />

                            <button
                                type="button"
                                className="btn btn-danger"
                                onClick={() => eliminarHorario(index)}
                                style={{ width: "48px", padding: "0" }}
                            >
                                X
                            </button>
                        </div>
                    ))}
                </div>

                <button
                    type="button"
                    className="btn btn-secondary w-100"
                    onClick={agregarHorario}
                >
                    + Agregar horario
                </button>
            </div>

            <button
                className="btn btn-primary btn-large w-100 mb-4"
                onClick={guardarCambios}
                disabled={loading}
            >
                {loading ? "Guardando..." : "Guardar cambios"}
            </button>
        </div>
    );
}

export default EditarHorarios;
