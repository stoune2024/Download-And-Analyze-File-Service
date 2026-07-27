export function createDownloadEvents() {
    return new EventSource(
        "http://localhost:8000/download/events"
    );
}