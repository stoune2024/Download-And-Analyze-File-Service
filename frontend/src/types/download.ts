export interface DownloadProgress {

    received_names: number;

    downloaded_files: number;

    total_downloaded: number;
}

export interface DownloadResult {

    status: string;

    downloaded: number;

    retry_after?: number;
}