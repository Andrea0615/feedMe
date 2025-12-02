import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={styles.nav}>
      <h3>FeedMe 🐾</h3>

      <div>
        <button onClick={() => navigate("/home")}>Home</button>
        <button onClick={() => navigate("/perfil")}>Mi Perfil</button>
        <button onClick={handleLogout} style={styles.logout}>
          Cerrar sesión
        </button>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px 20px",
    background: "#0d6efd",
    color: "white",
  },
  logout: {
    marginLeft: "10px",
    background: "#dc3545",
    color: "white",
    border: "none",
    padding: "6px 10px",
    cursor: "pointer",
  },
};

export default Navbar;
