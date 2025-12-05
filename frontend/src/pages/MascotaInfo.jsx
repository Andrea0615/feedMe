import { useEffect, useState } from "react";
import { getMascotaInfo } from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/mascota.css";


function MascotaInfo() {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getMascotaInfo();
                setData(res.data);
            } catch (err) {
                console.log(err);
                navigate("/");
            }
        }
        load();
    }, []);

    if (!data) return <div className="container mt-4">Cargando...</div>;

    return (
        <div className="container mt-4 mb-4">
            <div className="detalles-header">
                <h2>Detalles</h2>
                <button
                    className="btn-edit-mascota"
                    onClick={() => navigate("/editar-mascota")}
                    title="Editar mascota"
                >
                    <i className="fas fa-edit"></i>
                </button>
            </div>

            <div className="pet-card-full">
                <img
                    src={data.mascota.foto || "https://www.poresto.com/crop/0-0-1140-855O1F0x0D1024x0C8846c116bc66478c0a67848c160cc0d5/media/fotografias/fotosnoticias/2021/11/29/157336.jpg"}
                    alt={data.mascota.nombre}
                    className="pet-image-full"
                />

                <div className="pet-name-row">
                    <h2 className="pet-name-full">{data.mascota.nombre}</h2>

                    <button
                        className="btn-view-camera"
                        onClick={() => navigate("/ver-camara")}
                    >
                        Ver
                    </button>
                </div>

                <div className="pet-badges">
                    <span className="badge-item">
                        <span className="badge-label"><i className="fas fa-birthday-cake"></i> Edad</span>
                        <span className="badge-value">{data.mascota.edad} años</span>
                    </span>
                    <span className="badge-item">
                        <span className="badge-label"><i className="fas fa-weight"></i> Peso</span>
                        <span className="badge-value">{data.mascota.peso_kg} kg</span>
                    </span>
                </div>
            </div>

            <div className="card mb-4">
                <div className="card-header-with-btn">
                    <h5>Horarios de comida</h5>
                    <button
                        className="btn-edit-card"
                        onClick={() => navigate("/horarios/editar")}
                        title="Editar horarios"
                    >
                        <i className="fas fa-edit"></i>
                    </button>
                </div>
                <div className="card-body">
                    <div className="schedule-list">
                        {data.horarios.map((h, i) => (
                            <div key={i} className="schedule-item">
                                <span className="schedule-time">{h.hora}</span>
                                <span className="schedule-portion">{h.porcion} g</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default MascotaInfo;
