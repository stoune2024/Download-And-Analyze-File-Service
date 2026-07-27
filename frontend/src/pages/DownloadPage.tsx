import { useState } from "react";

import { startDownload } from "../api/downloadApi";

import { DownloadButton } from "../components/download/DownloadButton";

import { DownloadProgress } from "../components/download/DownloadProgress";

import { useDownloadEvents } from "../hooks/useDownloadEvents";

export default function DownloadPage() {

    const [loading, setLoading] = useState(false);

    const [progress, setProgress] = useState({

        received_names: 0,

        downloaded_files: 0,

        total_downloaded: 0,

    });

    useDownloadEvents(

        loading,

        setProgress,

        () => setLoading(false),

    );

    async function handleDownload() {

        setLoading(true);

        await startDownload();

    }

    return (

        <>

            <h1>

                Download

            </h1>

            <DownloadButton

                loading={loading}

                onClick={handleDownload}

            />

            <DownloadProgress

                progress={progress}

            />

        </>

    );

}