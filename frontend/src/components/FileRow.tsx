import {
    FileItem
} from "../../types/file";


interface Props {

    file: FileItem;

    checked: boolean;

    onChange(
        id:number
    ):void;

}



export function FileRow({

    file,

    checked,

    onChange,

}:Props){


    return (

        <tr>


            <td>

                <input

                    type="checkbox"

                    checked={checked}

                    onChange={()=>
                        onChange(file.id)
                    }

                />

            </td>


            <td>

                {file.name}

            </td>


            <td>

                {
                    new Date(
                        file.downloaded_at
                    )
                    .toLocaleString()
                }

            </td>


        </tr>

    );

}