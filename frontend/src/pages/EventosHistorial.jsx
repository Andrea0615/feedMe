import { useEffect, useState } from "react";
import { getEventosHistorial } from "../services/api";
import { useNavigate } from "react-router-dom";

function EventosHistorial() {
    const [eventos, setEventos] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getEventosHistorial();
                setEventos(res.data);
            } catch (err) {
                console.log(err);
                navigate("/login");
            } finally {
                setLoading(false);
            }
        }
        load();
    }, []);

    if (loading) return <div className="container mt-4">Cargando...</div>;

    return (
        <div className="container mt-4">
            <h2>Historial de Eventos</h2>

            {eventos.length === 0 ? (
                <p className="mt-4 text-muted">No hay eventos registrados aún.</p>
            ) : (
                <div className="list-group mt-3">
                    {eventos.map((ev, idx) => (
                        <div 
                            key={idx}
                            className="list-group-item d-flex flex-column"
                            style={{
                                borderLeft: 
                                    ev.prioridad === 3 ? "6px solid #ff4d4d" :
                                    ev.prioridad === 2 ? "6px solid #ffae00" :
                                    "6px solid #1e90ff"
                            }}
                        >
                            <strong>{ev.tipo_evento}</strong>
                            <span className="text-muted">{ev.fecha}</span>

                            <small className="mt-2">
                                Prioridad:{" "}
                                <span 
                                    style={{
                                        fontWeight: "bold",
                                        color:
                                            ev.prioridad === 3 ? "#ff4d4d" :
                                            ev.prioridad === 2 ? "#ffae00" :
                                            "#1e90ff"
                                    }}
                                >
                                    {ev.prioridad}
                                </span>
                            </small>
                        </div>
                    ))}
                </div>
            )}

            <button 
                className="btn btn-secondary mt-4"
                onClick={() => navigate("/home")}
            >
                Volver
            </button>
        </div>
    );
}

export default EventosHistorial;
