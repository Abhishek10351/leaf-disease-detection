import axios from "axios";
import cookies from "js-cookie";
import 'dotenv/config';


const baseURL = "http://127.0.0.1:8000/";

const finalBaseURL = process.env.NEXT_PUBLIC_API_BASE_URL || baseURL;

const api = axios.create({
    baseURL: finalBaseURL,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config) => {
        const accessToken = cookies.get("authToken");
        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);
export { finalBaseURL };
export default api;
