import type { DownloadProgress as Progress } from "../../types/download";


interface Props {
    progress: Progress;
}


export function DownloadProgress(
    {
        progress,
    }: Props
) {

    return (
        <div>

            <p>
                Получено имен:
                {progress.received_names}
            </p>


            <p>
                Скачано файлов:
                {progress.downloaded_files}
            </p>


            <p>
                Всего:
                {progress.total_downloaded}
            </p>

        </div>
    );
}