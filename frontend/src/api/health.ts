import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export async function getHealth() {
    const response = await api.get("/");

    return response.data;
}