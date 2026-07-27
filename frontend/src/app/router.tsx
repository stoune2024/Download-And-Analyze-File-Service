import {

    BrowserRouter,

    Routes,

    Route,

} from "react-router-dom";

import DownloadPage from "../pages/DownloadPage";

export function Router() {

    return (

        <BrowserRouter>

            <Routes>

                <Route

                    path="/"

                    element={<DownloadPage />}

                />

            </Routes>

        </BrowserRouter>

    );

}