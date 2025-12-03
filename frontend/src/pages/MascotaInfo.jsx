import { useEffect, useState } from "react";
import { getMascotaInfo } from "../services/api";
import { useNavigate } from "react-router-dom";

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
        <div className="container mt-4">
            <h2>Mascota: {data.mascota.nombre}</h2>

            <div className="card p-3 mt-3">
                <h5>Información</h5>
                <p>Edad: {data.mascota.edad} años</p>
                <p>Peso: {data.mascota.peso_kg} kg</p>
            </div>

            <div className="card p-3 mt-3">
                <h5>Plan Alimenticio</h5>
            </div>

            <div className="card p-3 mt-3">
                <h5>Horarios</h5>
                {data.horarios.map((h, i) => (
                    <p key={i}>
                        {h.hora} — {h.porcion} g
                    </p>
                ))}
            </div>

            <button
                className="btn btn-secondary mt-4"
                onClick={() => navigate("/")}
            >
                Volver
            </button>

            <button
                className="btn btn-primary mt-4"
                onClick={() => navigate("/editar-mascota")}
            >
                Editar Mascota
            </button>

        </div>
    );
}

export default MascotaInfo;
