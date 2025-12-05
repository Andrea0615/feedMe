import { useEffect, useState } from "react";
import { getMascotaInfo, actualizarMascota } from "../services/api";
import { useNavigate } from "react-router-dom";

function EditMascota() {
    const [nombre, setNombre] = useState("");
    const [edad, setEdad] = useState("");
    const [peso, setPeso] = useState("");
    const [objetivo, setObjetivo] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const objetivos = [
        "Mantener peso",
        "Bajar de peso",
        "Subir de peso",
        "Cachorro activo",
        "Adulto mayor"
    ];

    useEffect(() => {
        async function load() {
            try {
                const res = await getMascotaInfo();
                const m = res.data.mascota;

                setNombre(m.nombre);
                setEdad(m.edad);
                setPeso(m.peso_kg);
                setObjetivo(m.objetivo || "");
            } catch (err) {
                console.log(err);
                navigate("/");
            }
        }
        load();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            await actualizarMascota({
                nombre,
                edad: Number(edad),
                peso_kg: Number(peso),
                objetivo
            });

            alert("Mascota actualizada ✅");
            navigate("/ver-mascota");
        } catch (err) {
            console.log(err);
            alert("Error actualizando mascota");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4 mb-4">
            <h2>Editar Mascota</h2>

            <form className="card p-4" onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Nombre</label>
                    <input
                        className="form-control"
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
                        required
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
                        required
                    />
                </div>

                <div className="mb-4">
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

                <button className="btn btn-primary btn-large w-100" disabled={loading}>
                    {loading ? "Guardando..." : "Guardar cambios"}
                </button>
            </form>
        </div>
    );
}

export default EditMascota;
