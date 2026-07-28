import { api } from "./axios";
import type { FilesResponse } from "../types/file";

export async function getFiles(
    page: number,
    size: number,
): Promise<FilesResponse> {
    const response = await api.get<FilesResponse>(
        "/files",
        {
            params: {
                page,
                size,
            },
        },
    );

    return response.data;
}