import { DownloadProgress as Progress } from "../../types/download";

interface Props {

    progress: Progress;

}

export function DownloadProgress({

    progress,

}: Props) {

    return (

        <>

            <p>

                Получено имен:

                {progress.received_names}

            </p>

            <p>

                Скачано из пачки:

                {progress.downloaded_files}

            </p>

            <p>

                Всего скачано:

                {progress.total_downloaded}

            </p>

            <progress

                value={progress.downloaded_files}

                max={progress.received_names}

            />

        </>

    );

}