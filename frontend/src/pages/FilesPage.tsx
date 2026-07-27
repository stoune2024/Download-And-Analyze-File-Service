import {
    useState
} from "react";


import {
    useFiles
} from "../hooks/useFiles";


import {
    FilesTable
} from "../components/files/FilesTable";


import {
    Pagination
} from "../components/files/Pagination";



export default function FilesPage(){


const size = 20;


const [page,setPage] = useState(1);


const {

files,

total,

loading,

}=useFiles(

page,

size

);



const [

selected,

setSelected

]=useState<number[]>([]);



function toggle(id:number){


setSelected(prev=>


prev.includes(id)

?

prev.filter(
    x=>x!==id
)

:

[
    ...prev,
    id
]


);


}



function togglePage(){


const ids = files.map(
    x=>x.id
);



const all = ids.every(
    x=>selected.includes(x)
);



if(all){

    setSelected(
        selected.filter(
            x=>!ids.includes(x)
        )
    );

}

else{


    setSelected(

        [

        ...new Set(
            [
                ...selected,
                ...ids
            ]
        )

        ]

    );

}


}



return (

<div>


<h1>
Files
</h1>


{
loading &&
<p>
Loading...
</p>
}


<FilesTable


files={files}


selected={selected}


toggle={toggle}


togglePage={togglePage}


allSelected={

files.length>0 &&

files.every(
x=>selected.includes(x.id)
)

}


/>


<Pagination


page={page}


size={size}


total={total}


change={setPage}


/>


<p>

Выбрано:

{selected.length}

</p>


</div>

);


}