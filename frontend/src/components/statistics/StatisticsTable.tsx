import type {
    DigitStatistics
} from "../../types/statistics";



interface Props {

    title:string;

    statistics:DigitStatistics;

}



export function StatisticsTable({

    title,

    statistics,

}:Props){


return (

<div>


<h3>

{title}

</h3>


<table>


<thead>

<tr>

<th>
Цифра
</th>

<th>
Количество
</th>

</tr>

</thead>



<tbody>


{
Object.entries(
    statistics.counts
)
.map(
([digit,count])=>(


<tr key={digit}>


<td>

{digit}

</td>


<td>

{count}

</td>


</tr>


)

)

}


</tbody>


</table>


</div>

);


}