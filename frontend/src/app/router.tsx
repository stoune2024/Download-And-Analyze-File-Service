import {

    BrowserRouter,

    Routes,

    Route,

} from "react-router-dom";

import DownloadPage from "../pages/DownloadPage";
import FilesPage from "../pages/FilesPage";

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

            </Routes>

        </BrowserRouter>

    );

}