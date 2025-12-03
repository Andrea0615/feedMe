import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function PrivateRoute({ children }) {
    const isLoggedIn = useAuth();

    // si NO esta logged in → redirige al login
    if (!isLoggedIn) {
        return <Navigate to="/login" replace />;
    }

    // si sí está logged in → muestra la página protegida
    return children;
}
