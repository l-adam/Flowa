const configUrl = '/backend/export/configuration_example.json';

var config;
var exportUrl;
var dataSourcesPath;
var dataOverlaysPath;
var dataSources;
var dataOverlays;
var timelines;
var defaults;

function getJSON(url) {
	var resp;
	var xmlHttp;

	resp = '';
	xmlHttp = new XMLHttpRequest();

	if (xmlHttp != null) {
		xmlHttp.open("GET", url, false);
		xmlHttp.send(null);
		resp = xmlHttp.responseText;
		return JSON.parse(resp);
	}

	return resp;
}

function parseConfig() {
	config = getJSON(configUrl);

	dataSourcesPath = config.serverConfiguration.dataSourcesPath;
	dataOverlaysPath = config.serverConfiguration.dataOverlaysPath;

	dataSources = config.dataSources.items;
	dataOverlays = config.dataSources.items;
	timelines = config.timeline.items;
	defaults = config.defaults;
}

function parseGeoJSONUrl(index, type, timelineIndex) {
	var geoJSONUrl = '';
	var dataName;

	if (type == 'source') {
		dataName = dataSources[index].id;
	} else if (type == 'overlay') {
		dataName = dataOverlays[index].id;
	}

	geoJSONUrl = dataSourcesPath + dataName + '_' +
		timelines[timelineIndex].id + '.geojson';

	return geoJSONUrl;
}
