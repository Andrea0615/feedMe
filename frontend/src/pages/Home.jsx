import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHomeInfo } from "../services/api";

function Home() {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getHomeInfo();
                setData(res.data);
            } catch (error) {
                console.log(error);
                navigate("/login");
            }
        }
        load();
    }, []);

    if (!data) return <div className="container mt-4">Cargando...</div>;

    return (
        <div className="container mt-4">

            {/* Icono perfil */}
            <div className="d-flex justify-content-end">
                <button 
                    className="btn btn-outline-secondary"
                    onClick={() => navigate("/perfil")}
                >
                    Perfil
                </button>
            </div>

            <h2 className="mt-3">Hola, {data.nombre_usuario} 👋</h2>

            {!data.tiene_mascota ? (
                <div className="mt-4">
                    <p>Aún no has registrado una mascota.</p>
                    <button 
                        className="btn btn-primary w-100"
                        onClick={() => navigate("/registrar-mascota")}
                    >
                        Registrar Mascota
                    </button>
                </div>
            ) : (
                <>
                    <div className="card p-3 mt-4">
                        <h4>Próxima comida</h4>
                        <p className="fs-5">
                            {data.proxima_comida ?? "No hay horarios configurados"}
                        </p>
                    </div>

                    <div className="d-flex flex-column gap-3 mt-4">
                        <button 
                            className="btn btn-primary"
                            onClick={() => navigate("/ver-mascota")}
                        >
                            Ver Mascota
                        </button>

                        <button 
                            className="btn btn-secondary"
                            onClick={() => navigate("/editar-plan")}
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
