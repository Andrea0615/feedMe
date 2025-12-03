// Este codigo regresa si estas logged in o no

export default function useAuth() {
    const token = localStorage.getItem("token");
    return !!token; // true si hay token, false si no
}
