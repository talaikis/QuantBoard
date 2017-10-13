import { tsvParse, csvParse } from  "d3-dsv";
import { timeParse } from "d3-time-format";
import axios from 'axios';

function parseData(parse) {
	return function(d) {
		d.date = parse(d.date);
		d.open = +d.open;
		d.high = +d.high;
		d.low = +d.low;
		d.close = +d.close;
		d.volume = +d.volume;

		return d;
	};
}

const parseDate = timeParse("%Y-%m-%d");

export function getData() {
	const promise = axios.get('http://127.0.0.1:5000/api/v1.0/data/BTCUSD/LVAR/200')
		.then(response => response.data)
		.then(data => tsvParse(data, parseData(parseDate)))
	return promise;
}
