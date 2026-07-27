import {
    FileItem
} from "../../types/file";


import {
    FileRow
} from "./FileRow";


interface Props {

    files: FileItem[];

    selected:number[];

    toggle(id:number):void;

    togglePage():void;

    allSelected:boolean;

}



export function FilesTable({

    files,

    selected,

    toggle,

    togglePage,

    allSelected,

}:Props){


return (

<table>


<thead>

<tr>

<th>

<input

type="checkbox"

checked={allSelected}

onChange={togglePage}

/>

</th>


<th>
Имя
</th>


<th>
Дата
</th>


</tr>

</thead>


<tbody>


{
files.map(file=>(


<FileRow

key={file.id}

file={file}

checked={
    selected.includes(
        file.id
    )
}

onChange={toggle}

/>


))

}


</tbody>


</table>

);

}