export interface DigitStatistics {

    counts: Record<string, number>;

}



export interface FileStatistics {

    id: number;

    name: string;

    statistics: DigitStatistics;

}



export interface StatisticsResponse {

    total: DigitStatistics;

    files: FileStatistics[];

}