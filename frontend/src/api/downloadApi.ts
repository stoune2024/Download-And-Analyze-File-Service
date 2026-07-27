import { api } from "./axios";

export const startDownload = async () => {

    await api.post("/download");

};