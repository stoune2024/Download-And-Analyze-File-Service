export class DownloadEvents {

    private source?: EventSource;

    connect(

        onProgress: (data: any) => void,

        onFinish: () => void,

    ) {

        this.source = new EventSource(

            "http://localhost:8000/download/events"

        );

        this.source.addEventListener(

            "downloaded",

            event => {

                onProgress(

                    JSON.parse(event.data)

                );

            }

        );

        this.source.addEventListener(

            "finished",

            () => {

                onFinish();

            }

        );

    }

    disconnect() {

        this.source?.close();

    }

}