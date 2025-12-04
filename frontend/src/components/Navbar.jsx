import { Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import "../styles/navbar.css";

function Navbar() {
    const isLoggedIn = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <nav className="navbar-mobile">
            <div className="navbar-content">
                <Link className="navbar-brand" to="/">
                    🐾 FeedMe
                </Link>

                <div className="navbar-actions">
                    {isLoggedIn && (
                        <Link className="nav-link" to="/ver-perfil">
                            👤
                        </Link>
                    )}

                    {!isLoggedIn ? (
                        <Link className="btn btn-nav-primary" to="/login">
                            Login
                        </Link>
                    ) : (
                        <button className="btn btn-nav-logout" onClick={handleLogout}>
                            Logout
                        </button>
                    )}
                </div>
            </div>
        </nav>
    );
}


export default Navbar;
