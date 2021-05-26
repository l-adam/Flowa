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

function getJSONZip(url, filename) {
	var geoJSONData;

	var promise = new JSZip.external.Promise(function(resolve, reject) {
		JSZipUtils.getBinaryContent(url + '.zip', function(err, data) {
			if (err) {
				reject(err);
			} else {
				resolve(data);
			}
		});
	});

	geoJSONData = promise.then(JSZip.loadAsync)
		.then(function(zip) {
			return zip.file(filename).async("string");
		})
		.then(function success(text) {
			return JSON.parse(text);
		}, function error(e) {});

	return geoJSONData;
}

async function parseConfig() {
	config = getJSON(configUrl);

	dataSourcesPath = config.serverConfiguration.dataSourcesPath;
	dataOverlaysPath = config.serverConfiguration.dataOverlaysPath;

	dataSources = config.dataSources.items;
	dataOverlays = config.dataOverlays.items;
	timelines = config.timeline.items;
	defaults = config.defaults;

	generateIndices(dataSources);
	generateIndices(dataOverlays);

	parseDefaults();

	assetsConfig = getJSON(assetsConfigUrl);

	return 0;
}

function parseDefaults() {
	current.dataSource = dataSources[defaults.dataSourceIndex];
	current.timelineIndex = defaults.timelineIndex;
	current.dataOverlays = dataOverlays;

	dataOverlays.forEach((dataOverlay, index) => {
		current.dataOverlays[index].visibility = dataOverlay.defaultVisibility;
	});
}

function parseGeoJSONUrl({
	index,
	type,
	timelineIndex
}) {
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

	return new Promise((resolve) => {
		resolve(geoJSONUrl);
	});
}

function parseGeoJSONZip({
	index,
	type,
	timelineIndex
}) {
	var geoJSON;
	var geoJSONUrl = '';
	var geoJSONFile = '';
	var dataName;
	var dataPath;

	if (type == 'source') {
		dataName = dataSources[index].id;
		dataPath = dataSourcesPath;
	} else if (type == 'overlay') {
		dataName = dataOverlays[index].id;
		dataPath = dataOverlaysPath;
	}

	geoJSONFile = dataName + '_' +
		timelines[timelineIndex].id + '.geojson';

	geoJSONUrl = dataPath + geoJSONFile;

	geoJSON = getJSONZip(geoJSONUrl, geoJSONFile);
	return geoJSON;
}

function generateIndices(data) {
	data.forEach(
		(data, index) => {
			data.index = index;
		});
}
