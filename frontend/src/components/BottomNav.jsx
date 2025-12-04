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
                ←
            </button>

            <button 
                className="nav-btn nav-home" 
                onClick={handleHome}
                title="Inicio"
            >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                </svg>
            </button>

            <button 
                className="nav-btn nav-forward" 
                onClick={handleForward}
                title="Siguiente"
            >
                →
            </button>
        </nav>
    );
}

export default BottomNav;
