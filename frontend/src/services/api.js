import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:5001/api",
});

// Auto-agregar token a TODAS las peticiones
API.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});


// REGISTER USER
export function registerUser(data) {
    return API.post("/auth/register", data);
}

// LOGIN USER
export function loginUser(data) {
    return API.post("/auth/login", data);
}

// REGISTER PET
export function registrarMascota(data) {
    return API.post("/mascota/register", data);
}

export function getHomeInfo() {
    return API.get("/home");
}

export function getMascotaInfo() {
    return API.get("/mascota/info");
}

export function actualizarMascota(data) {
    return API.put("/mascota/edit", data);
}

export function getUserInfo() {
    return API.get("/user/info");
}

export function updateUserInfo(data) {
    return API.put("/user/edit", data);
}



export default API;
