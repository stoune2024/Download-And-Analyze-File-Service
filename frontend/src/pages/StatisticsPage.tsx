import {
    useLocation
} from "react-router-dom";


import {
    useEffect,
    useState
} from "react";


import {
    calculateStatistics
} from "../api/statisticsApi";


import type {
    StatisticsResponse
} from "../types/statistics";


import {
    StatisticsTable
} from "../components/statistics/StatisticsTable";


import {
    FileStatisticsTable
} from "../components/statistics/FileStatisticsTable";



export default function StatisticsPage(){



const location = useLocation();



const ids:number[] =

location.state?.fileIds ?? [];



const [

statistics,

setStatistics

]=useState<StatisticsResponse|null>(null);



const [

loading,

setLoading

]=useState(false);




useEffect(()=>{


async function load(){


if(ids.length===0)

    return;



setLoading(true);



const result = await calculateStatistics(ids);



setStatistics(result);



setLoading(false);



}



load();



},[]);




if(loading)

return (

<p>

Расчет...

</p>

);




if(!statistics)

return (

<p>

Файлы не выбраны

</p>

);




return (

<div>


<h1>

Статистика

</h1>



<StatisticsTable


title="Общая статистика"


statistics={
    statistics.total
}


/>



<h1>

По файлам

</h1>



{

statistics.files.map(file=>(


<FileStatisticsTable

key={file.id}

file={file}


/>


))


}


</div>

);


}