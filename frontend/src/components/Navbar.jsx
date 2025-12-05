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
                    <i className="fas fa-paw"></i> FeedMe
                </Link>

                <div className="navbar-actions">
                    {isLoggedIn && (
                        <Link className="nav-link" to="/ver-perfil">
                            <i className="fas fa-user"></i>
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
export default Navbar;
