import {
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";


import {
    useFiles
} from "../hooks/useFiles";


import {
    FilesTable
} from "../components/files/FilesTable";


import {
    Pagination
} from "../components/files/Pagination";



export default function FilesPage() {


    const navigate = useNavigate();


    const size = 20;


    const [page, setPage] = useState(1);



    const {
        files,
        total,
        loading,
    } = useFiles(
        page,
        size,
    );



    const [
        selected,
        setSelected
    ] = useState<number[]>([]);




    /**
     * Выбор одного файла
     */
    function toggleFile(
        id: number
    ) {


        setSelected(
            previous => {


                if (
                    previous.includes(id)
                ) {

                    return previous.filter(
                        item => item !== id
                    );

                }


                return [
                    ...previous,
                    id
                ];

            }
        );

    }




    /**
     * Выбор всех файлов на текущей странице
     */
    function togglePage() {


        const pageIds = files.map(
            file => file.id
        );


        const allSelected = pageIds.every(
            id => selected.includes(id)
        );



        if (allSelected) {


            setSelected(
                previous =>
                    previous.filter(
                        id =>
                            !pageIds.includes(id)
                    )
            );


            return;

        }



        setSelected(

            previous => [

                ...new Set(

                    [

                        ...previous,

                        ...pageIds

                    ]

                )

            ]

        );

    }





    /**
     * Переход на страницу статистики
     */
    function calculateStatistics() {


        navigate(

            "/statistics",

            {

                state: {

                    fileIds: selected

                }

            }

        );

    }




    const allPageSelected =

        files.length > 0 &&

        files.every(

            file =>
                selected.includes(file.id)

        );




    return (

        <div>


            <h1>
                Скачанные файлы
            </h1>



            {
                loading &&

                <p>
                    Загрузка...
                </p>
            }




            <FilesTable


                files={files}


                selected={selected}


                toggle={toggleFile}


                togglePage={togglePage}


                allSelected={allPageSelected}


            />





            <Pagination


                page={page}


                size={size}


                total={total}


                change={setPage}


            />





            <div>


                <p>

                    Выбрано файлов:

                    {" "}

                    {selected.length}

                </p>



                <button


                    disabled={
                        selected.length === 0
                    }


                    onClick={
                        calculateStatistics
                    }


                >

                    Произвести расчёты


                </button>


            </div>



        </div>

    );

}