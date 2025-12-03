import { useEffect, useState } from "react";
import { getMascotaInfo, actualizarMascota } from "../services/api";
import { useNavigate } from "react-router-dom";

function EditMascota() {
    const [nombre, setNombre] = useState("");
    const [edad, setEdad] = useState("");
    const [peso, setPeso] = useState("");

    const navigate = useNavigate();

    useEffect(() => {
        async function load() {
            try {
                const res = await getMascotaInfo();
                const m = res.data.mascota;

                setNombre(m.nombre);
                setEdad(m.edad);
                setPeso(m.peso_kg);
            } catch (err) {
                console.log(err);
                navigate("/");
            }
        }
        load();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await actualizarMascota({
                nombre,
                edad: Number(edad),
                peso_kg: Number(peso)
            });

            alert("Mascota actualizada");
            navigate("/ver-mascota");
        } catch (err) {
            console.log(err);
            alert("Error actualizando mascota");
        }
    };

    return (
        <div className="container mt-4">
            <h2>Editar Mascota</h2>

            <form className="mt-3" onSubmit={handleSubmit}>
                <input
                    className="form-control mb-2"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />

                <input
                    className="form-control mb-2"
                    type="number"
                    value={edad}
                    onChange={(e) => setEdad(e.target.value)}
                />

                <input
                    className="form-control mb-2"
                    type="number"
                    step="0.1"
                    value={peso}
                    onChange={(e) => setPeso(e.target.value)}
                />

                <button className="btn btn-primary w-100 mt-3">
                    Guardar cambios
                </button>
            </form>
        </div>
    );
}

export default EditMascota;
