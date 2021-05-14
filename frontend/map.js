mapboxgl.accessToken = 'pk.eyJ1IjoiczM1NzU1NiIsImEiOiJja201NTJvdnEwYjZuMm90cHNvOXllaG43In0.oPyg05LFrXhKR5Zmd_LJzQ';

parseConfig();

var map = new mapboxgl.Map({
	container: 'map', // container ID
	style: 'mapbox://styles/mapbox/streets-v11', // style URL
	center: [10.743942, 59.918721], // starting position
	zoom: 12, // starting zoom
	antialias: false
});

var dataSourceOptions = {
	'index': defaults.dataSourceIndex,
	'type': 'source',
	'timelineIndex': defaults.timelineIndex
};

initializeHeatmap(dataSourceOptions, dataSources[defaults.dataSourceIndex].colorScheme, -2, 2);

map.once('load', function() {
	initializeOverlays();
});
