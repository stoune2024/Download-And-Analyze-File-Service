import { useEffect } from "react";

import { DownloadEvents } from "../services/downloadEvents";

export function useDownloadEvents(

    enabled: boolean,

    onProgress: (progress: any) => void,

    onFinish: () => void,

) {

    useEffect(() => {

        if (!enabled)
            return;

        const events = new DownloadEvents();

        events.connect(

            onProgress,

            onFinish,

        );

        return () => events.disconnect();

    }, [enabled]);

}