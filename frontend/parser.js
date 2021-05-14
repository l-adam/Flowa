const configUrl = '/backend/export/configuration_example.json';
const assetsConfigUrl = '/frontend/assets/config.json';

var config;
var exportUrl;
var dataSourcesPath;
var dataOverlaysPath;
var dataSources;
var dataOverlays;
var timelines;
var defaults;
var assetsConfig;

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
	dataOverlays = config.dataOverlays.items;
	timelines = config.timeline.items;
	defaults = config.defaults;

	assetsConfig = getJSON(assetsConfigUrl);
}

function parseGeoJSONUrl({index, type, timelineIndex}) {
	var geoJSONUrl = '';
	var dataName;
	var dataPath;

	if (type == 'source') {
		dataName = dataSources[index].id;
		dataPath = dataSourcesPath;
	} else if (type == 'overlay') {
		dataName = dataOverlays[index].id;
		dataPath = dataOverlaysPath;
	}

	geoJSONUrl = dataPath + dataName + '_' +
		timelines[timelineIndex].id + '.geojson';

	return geoJSONUrl;
}
