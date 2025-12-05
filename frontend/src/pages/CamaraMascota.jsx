import { useRef, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getMascotaInfo } from "../services/api";
import "../styles/camara.css";

function CamaraMascota() {
    const iframeRef = useRef(null);
    const cameraIP = "172.20.10.3:81/stream";
    const navigate = useNavigate();
    const [nombreMascota, setNombreMascota] = useState("");

    useEffect(() => {
        if (iframeRef.current) {
            iframeRef.current.src = `http://${cameraIP}`;
        }

        // Obtener nombre de la mascota
        getMascotaInfo()
            .then(res => setNombreMascota(res.data.mascota.nombre))
            .catch(() => setNombreMascota("tu mascota"));
    }, [cameraIP]);

    return (
        <div className="camara-container">
            <div className="camara-header">
                <h2>¡Saluda a {nombreMascota}! 👋</h2>
                <button 
                    className="btn-close"
                    onClick={() => navigate("/ver-mascota")}
                    title="Cerrar"
                >
                    ✕
                </button>
            </div>

            <div className="camara-content">
                <div className="camara-status">
                    <span className="status-dot"></span>
                    <span style={{ color: '#10b981', fontSize: '0.85rem', fontWeight: '600' }}>En vivo</span>
                </div>
                
                <iframe
                    ref={iframeRef}
                    className="camara-iframe"
                    title="Cámara ESP32"
                    frameBorder="0"
                    allowFullScreen
                />
            </div>

            <div className="camara-controls">
                <button 
                    className="btn-control btn-volver"
                    onClick={() => navigate("/ver-mascota")}
                >
                    ← Volver
                </button>
            </div>
        </div>
    );
}

export default CamaraMascota;
