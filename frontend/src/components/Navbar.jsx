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
        <nav
            className="navbar px-3"
            style={{
                backgroundColor: "#ffffff",
                borderBottom: "1px solid #eee",
                height: "60px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                position: "sticky",
                top: 0,
                zIndex: 100,
            }}
        >
            <Link className="navbar-brand fw-bold" to="/" style={{ fontSize: "20px" }}>
                FeedMe 🐶
            </Link>

            <div className="d-flex gap-3">
                {isLoggedIn && (
                    <Link className="text-decoration-none" to="/home">
                        Home
                    </Link>
                )}

                {!isLoggedIn ? (
                    <Link className="btn btn-primary btn-sm" to="/login">
                        Login
                    </Link>
                ) : (
                    <button className="btn btn-danger btn-sm" onClick={handleLogout}>
                        Logout
                    </button>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
