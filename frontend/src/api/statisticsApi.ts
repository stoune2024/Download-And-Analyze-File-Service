import { api } from "./axios";

import type {
    StatisticsResponse
} from "../types/statistics";


export async function calculateStatistics(

    fileIds:number[]

):Promise<StatisticsResponse>{


    const response = await api.post(

        "/statistics",

        {
            file_ids:fileIds
        }

    );


    return response.data;

}