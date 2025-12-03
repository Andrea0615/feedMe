import { Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

function Navbar() {
    const isLoggedIn = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <nav className="navbar navbar-light bg-light px-3">
            <Link className="navbar-brand" to="/">FeedMe 🐶</Link>

            <div>
                {!isLoggedIn ? (
                    <Link className="btn btn-primary" to="/login">
                        Login
                    </Link>
                ) : (
                    <button className="btn btn-danger" onClick={handleLogout}>
                        Logout
                    </button>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
