import * as d3 from 'd3';
import { base } from "$app/paths";

const DATA_PATH = 'data';

export async function loadData(){
    let data = await d3.json(`${base}/${DATA_PATH}/data.json`, d3.autoType);
    return data
}
