import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHomeInfo } from "../services/api";

function Home() {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getHomeInfo()
            .then(res => setData(res.data))
            .catch(() => navigate("/login"));
    }, []);

    if (!data) return <div className="text-center mt-4">Cargando...</div>;

    return (
        <div className="container mt-4" style={{ maxWidth: "450px" }}>
            
            <h2 className="fw-bold mb-3">Hola, {data.nombre_usuario} 👋</h2>

            {!data.tiene_mascota ? (
                <div
                    className="p-4 rounded text-center"
                    style={{ backgroundColor: "#fff", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}
                >
                    <p className="mb-3">Aún no has registrado una mascota.</p>

                    <button
                        className="btn btn-primary w-100 py-2"
                        onClick={() => navigate("/registrar-mascota")}
                    >
                        Registrar Mascota
                    </button>
                </div>
            ) : (
                <>
                    <div
                        className="p-4 rounded mb-4"
                        style={{ backgroundColor: "#fff", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}
                    >
                        <h5>Próxima comida</h5>
                        <p className="fs-5 mt-2">
                            {data.proxima_comida ?? "Sin horarios"}
                        </p>
                    </div>

                    <div className="d-flex flex-column gap-3">
                        <button
                            className="btn btn-primary py-2"
                            onClick={() => navigate("/ver-mascota")}
                        >
                            Ver Mascota
                        </button>

                        <button
                            className="btn btn-secondary py-2"
                            onClick={() => navigate("/horarios/editar")}
                        >
                            Editar Horario
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default Home;
