import { useEffect, useState } from "react";
import { getMascotaInfo, updateHorarios } from "../services/api";
import { useNavigate } from "react-router-dom";

function EditarHorarios() {
  const [horarios, setHorarios] = useState([]);
  const navigate = useNavigate();

  //cargar horarios actuales
  useEffect(() => {
    getMascotaInfo()
      .then(res => {
        setHorarios(res.data.horarios);
      })
      .catch(() => alert("Error al cargar horarios"));
  }, []);

  //Cambiar un campo específico
  const cambiarHorario = (index, campo, valor) => {
    const copia = [...horarios];
    copia[index][campo] = valor;
    setHorarios(copia);
  };

  //Agregar nuevo horario
  const agregarHorario = () => {
    setHorarios([...horarios, { hora: "", porcion: "" }]);
  };

  //Eliminar horario
  const eliminarHorario = (index) => {
    const copia = horarios.filter((_, i) => i !== index);
    setHorarios(copia);
  };

  //Guardar cambios
  const guardarCambios = async () => {
    if (horarios.length === 0) {
      alert("Debes tener al menos un horario");
      return;
    }

    try {
      await updateHorarios(
        horarios.map(h => ({
          hora: h.hora,
          porcion: Number(h.porcion),
        }))
      );

      alert("Horarios actualizados ✅");
      navigate("/home");
    } catch (err) {
      alert("Error al guardar horarios");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Editar horarios de comida</h2>

      {horarios.map((h, index) => (
        <div key={index} style={{ display: "flex", gap: "10px", marginBottom: "8px" }}>
          <input
            type="time"
            value={h.hora}
            onChange={(e) => cambiarHorario(index, "hora", e.target.value)}
            required
          />

          <input
            type="number"
            placeholder="Porción (g)"
            value={h.porcion}
            onChange={(e) => cambiarHorario(index, "porcion", e.target.value)}
            required
          />

          <button onClick={() => eliminarHorario(index)}>🗑</button>
        </div>
      ))}

      <button onClick={agregarHorario}>+ Agregar horario</button>

      <hr />

      <button onClick={guardarCambios}>
        Guardar cambios
      </button>
    </div>
  );
}

export default EditarHorarios;
