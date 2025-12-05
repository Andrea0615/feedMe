import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHomeInfo, getMascotaInfo } from "../services/api";
import "../styles/home.css";

function Home() {
    const [data, setData] = useState(null);
    const [horarios, setHorarios] = useState([]);
    const [nombreMascota, setNombreMascota] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        async function loadData() {
            try {
                const res = await getHomeInfo();
                setData(res.data);
                
                // Obtener los horarios y nombre por separado
                if (res.data.tiene_mascota) {
                    const mascotaRes = await getMascotaInfo();
                    setHorarios(mascotaRes.data.horarios || []);
                    setNombreMascota(mascotaRes.data.mascota.nombre || "");
                }
            } catch (err) {
                console.log(err);
                navigate("/login");
            }
        }
        loadData();
    }, []);

    if (!data) return <div className="text-center mt-4">Cargando...</div>;

    return (
        <div className="home-container">
            <div className="home-header">
                <h2 className="greeting">Hola, {data.nombre_usuario} 👋</h2>
                <button
                    className="btn-notifications"
                    onClick={() => navigate("/eventos")}
                    title="Ver notificaciones"
                >
                    🔔
                </button>
            </div>

            {!data.tiene_mascota ? (
                <div className="home-content">
                    <div className="empty-state">
                        <div className="empty-icon">🐾</div>
                        <h3>Sin mascota registrada</h3>
                        <p>Comienza a registrar a tu mascota para gestionar sus horarios de comida</p>
                    </div>

                    <button
                        className="btn btn-primary btn-large"
                        onClick={() => navigate("/registrar-mascota")}
                    >
                        Registrar Mascota
                    </button>
                </div>
            ) : (
                <div className="home-content">
                    {/* Hero Pet Card */}
                    <div className="hero-pet-card">
                        <div className="hero-pet-image">
                            <img
                                src={data.mascota_foto || "https://www.poresto.com/crop/0-0-1140-855O1F0x0D1024x0C8846c116bc66478c0a67848c160cc0d5/media/fotografias/fotosnoticias/2021/11/29/157336.jpg"}
                                alt={data.nombre_mascota || nombreMascota}
                            />
                        </div>

                        <button
                            className="btn btn-primary btn-large w-100"
                            onClick={() => navigate("/ver-mascota")}
                        >
                            Ver a {nombreMascota || data.nombre_mascota || "tu mascota"}
                        </button>
                    </div>

                    {/* Feeding Schedule Section */}
                    <div className="feeding-section">
                        <div className="feeding-section-header">
                            <h3 className="section-title">Horarios de comida</h3>
                            <button
                                className="btn-edit-schedule"
                                onClick={() => navigate("/horarios/editar")}
                                title="Editar horarios"
                            >
                                ✎
                            </button>
                        </div>
                        <div className="feeding-schedule-box">
                            {horarios && horarios.length > 0 ? (
                                <div className="schedule-list-home">
                                    {horarios.map((h, i) => (
                                        <div key={i} className="schedule-item-home">
                                            <span className="schedule-time-home">{h.hora}</span>
                                            <span className="schedule-portion-home">{h.porcion} g</span>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="no-schedule">Sin horarios registrados</p>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Home;

