import {

    BrowserRouter,

    Routes,

    Route,

} from "react-router-dom";

import DownloadPage from "../pages/DownloadPage";
import FilesPage from "../pages/FilesPage";
import StatisticsPage from "../pages/StatisticsPage";
export function Router() {

    return (

        <BrowserRouter>

            <Routes>

                <Route

                    path="/"

                    element={<DownloadPage />}

                />
                <Route

                path="/files"

                element={<FilesPage/>}

                />
                <Route

                path="/statistics"

                element={<StatisticsPage/>}

                />

            </Routes>

        </BrowserRouter>

    );

}