const colorScale = ['#0000FF', '#773377', '#FF7700'];
const opacityScale = [0.5, 0.5, 0.5];

var firstSymbolId;
var currentHeatmapId;
let heatmapIds = ['heatmap', 'heatmap2'];

// Find the index of the first symbol layer in the map style
function findFirstLayer() {
	var layers = map.getStyle().layers;

	for (var i = 0; i < layers.length; i++) {
		if (layers[i].type === 'symbol') {
			firstSymbolId = layers[i].id;
			break;
		}
	}

	return firstSymbolId;
}

function addHeatmap(GeoJSONdata) {
	var heatmapOff;
	var heatmapOn;

	if (currentHeatmapId == heatmapIds[0]) {
		heatmapOff = heatmapIds[0];
		heatmapOn = heatmapIds[1]
		currentHeatmapId = heatmapIds[1];
	} else {
		heatmapOff = heatmapIds[1];
		heatmapOn = heatmapIds[0]
		currentHeatmapId = heatmapIds[0];
	}

	setHeatmap(heatmapOn, GeoJSONdata);

	map.once('data', function() {
		switchHeatmapVisibility(heatmapOff, heatmapOn);
	});
}

function switchHeatmapVisibility(heatmapOff, heatmapOn) {
	map.setLayoutProperty(heatmapOff, 'visibility', 'none');
	map.setLayoutProperty(heatmapOn, 'visibility', 'visible');
}

function addGeoJSONLayer(heatmapId, visibility, minStop, middleStop, maxStop) {
	map.addLayer({
			'id': heatmapId,
			'type': 'fill',
			'source': heatmapId, // reference the data source
			'layout': {
				'visibility': visibility
			},
			'paint': {
				'fill-color': {
					property: 'probability',
					stops: [
						[minStop, colorScale[0]],
						[middleStop, colorScale[1]],
						[maxStop, colorScale[2]]
					]
				},
				'fill-opacity': {
					property: 'probability',
					stops: [
						[minStop, opacityScale[0]],
						[middleStop, opacityScale[1]],
						[maxStop, opacityScale[2]]
					]
				},
				'fill-antialias': false,
			}
		},
		firstSymbolId);
}

function addGeoJSONSource(heatmapId, GeoJSONdata) {
	map.addSource(heatmapId, {
		'type': 'geojson',
		'data': GeoJSONdata
	});
}

function initializeHeatmap(GeoJSONdata, minStop, middleStop, maxStop) {
	map.once('load', function() {
		firstSymbolId = findFirstLayer();

		currentHeatmapId = heatmapIds[0];

		addGeoJSONSource(heatmapIds[0], GeoJSONdata);
		addGeoJSONSource(heatmapIds[1], '/backend/export/null.geojson');

		addGeoJSONLayer(heatmapIds[0], 'visible', minStop, middleStop, maxStop);
		addGeoJSONLayer(heatmapIds[1], 'none', minStop, middleStop, maxStop);
	})
}

function setHeatmap(heatmapId, GeoJSONdata) {
	map.getSource(heatmapId).setData(GeoJSONdata);
}
