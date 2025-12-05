import { useNavigate, useLocation } from "react-router-dom";
import "../styles/bottom-nav.css";

function BottomNav() {
    const navigate = useNavigate();
    const location = useLocation();

    // Don't show on login/register pages
    if (["/login", "/register"].includes(location.pathname)) {
        return null;
    }

    const handleBack = () => {
        navigate(-1);
    };

    const handleHome = () => {
        navigate("/home");
    };

    const handleForward = () => {
        navigate(1);
    };

    return (
        <nav className="bottom-nav">
            <button 
                className="nav-btn nav-back" 
                onClick={handleBack}
                title="Atrás"
            >
                <i className="fas fa-arrow-left"></i>
            </button>

            <button 
                className="nav-btn nav-home" 
                onClick={handleHome}
                title="Inicio"
            >
                <i className="fas fa-home"></i>
            </button>

            <button 
                className="nav-btn nav-forward" 
                onClick={handleForward}
                title="Siguiente"
            >
                <i className="fas fa-arrow-right"></i>
            </button>
        </nav>
    );
}

export default BottomNav;
