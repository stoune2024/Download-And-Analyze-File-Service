export interface FileItem {

    id: number;

    name: string;

    downloaded_at: string;

}


export interface FilesResponse {

    items: FileItem[];

    page: number;

    size: number;

    total: number;

}