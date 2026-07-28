import {
    useEffect,
    useState
} from "react";


import {
    getFiles
} from "../api/filesApi";


import type {
    FileItem,
} from "../types/file";

export function useFiles(

    page: number,

    size: number,

) {


    const [files, setFiles] = useState<FileItem[]>([]);


    const [total, setTotal] = useState(0);


    const [loading, setLoading] = useState(false);



    useEffect(() => {


        async function load() {

            setLoading(true);


            const data = await getFiles(

                page,

                size

            );


            setFiles(data.items);

            setTotal(data.total);


            setLoading(false);

        }


        load();


    }, [

        page,

        size

    ]);



    return {

        files,

        total,

        loading,

    };

}