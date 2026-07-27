import {
    BrowserRouter,
    Routes,
    Route,
    Link,
} from "react-router-dom";


import DownloadPage from "./pages/DownloadPage";
import FilesPage from "./pages/FilesPage";
import StatisticsPage from "./pages/StatisticsPage";


function App() {

    return (

        <BrowserRouter>

            <nav>

                <Link to="/">
                    Download
                </Link>

                {" | "}

                <Link to="/files">
                    Files
                </Link>

                {" | "}

                <Link to="/statistics">
                    Statistics
                </Link>

            </nav>


            <Routes>

                <Route
                    path="/"
                    element={
                        <DownloadPage />
                    }
                />


                <Route
                    path="/files"
                    element={
                        <FilesPage />
                    }
                />


                <Route
                    path="/statistics"
                    element={
                        <StatisticsPage />
                    }
                />

            </Routes>

        </BrowserRouter>

    );
}


export default App;