interface Props {

page:number;

size:number;

total:number;

change(page:number):void;

}



export function Pagination({

page,

size,

total,

change,

}:Props){


const pages = Math.ceil(

    total / size

);



return (

<div>


<button

disabled={page===1}

onClick={()=>
    change(page-1)
}

>

Назад

</button>


<span>

{page} / {pages}

</span>


<button

disabled={page===pages}

onClick={()=>
    change(page+1)
}

>

Вперед

</button>


</div>

);

}