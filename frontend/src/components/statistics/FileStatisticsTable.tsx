import type {
    FileStatistics
} from "../../types/statistics";


import {
    StatisticsTable
} from "./StatisticsTable";



interface Props {

    file:FileStatistics;

}



export function FileStatisticsTable({

    file

}:Props){


return (

<div>


<h2>

{file.name}

</h2>


<StatisticsTable

title=""

statistics={
    file.statistics
}

/>


</div>

);


}