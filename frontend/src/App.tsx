import { useEffect, useState } from "react";
import { getHealth } from "./api/health";

function App() {
    const [status, setStatus] = useState("Loading...");

    useEffect(() => {
        getHealth()
            .then((data) => {
                setStatus(data.status);
            })
            .catch(() => {
                setStatus("Backend unavailable");
            });
    }, []);

    return (
        <main
            style={{
                padding: 40,
                fontFamily: "sans-serif",
            }}
        >
            <h1>File Downloader</h1>

            <h2>Backend status:</h2>

            <p>{status}</p>
        </main>
    );
}

export default App;