import { useEffect } from "react";

import { createDownloadEvents } from "../api/sse";

export function useDownloadEvents(
    setProgress: (progress: DownloadProgress) => void,
) {

    useEffect(() => {

        const events = createDownloadEvents();

        events.addEventListener(
            "downloaded",
            (e) => {

                setProgress(
                    JSON.parse(e.data)
                );

            },
        );

        return () => {

            events.close();

        };

    }, []);
}