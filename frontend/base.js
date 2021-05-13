const defaultColorScheme = ['#0000FF', '#FF7700'];
const opacity = 0.5;

var firstSymbolId;
var currentHeatmapId;
var heatmapIds = ['heatmap', 'heatmap2'];

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

function changeHeatmap(GeoJSONdata, minStop, maxStop) {
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

	setHeatmapColorScale(defaultColorScheme, minStop, maxStop);

	map.once('data', function() {
		switchHeatmapVisibility(heatmapOff, heatmapOn);
	});
}

function switchHeatmapVisibility(heatmapOff, heatmapOn) {
	map.setLayoutProperty(heatmapOff, 'visibility', 'none');
	map.setLayoutProperty(heatmapOn, 'visibility', 'visible');
}

function addGeoJSONLayer(heatmapId, visibility, minStop, maxStop) {
	map.addLayer({
			'id': heatmapId,
			'type': 'fill',
			'source': heatmapId, // reference the data source
			'layout': {
				'visibility': visibility
			},
			'paint': {
				'fill-opacity': opacity,
				'fill-antialias': false
			},
		},
		firstSymbolId);
}

function addGeoJSONSource(heatmapId, GeoJSONdata) {
	map.addSource(heatmapId, {
		'type': 'geojson',
		'data': GeoJSONdata
	});
}

function initializeHeatmap(GeoJSONdata, colorScheme, minStop, maxStop) {
	map.once('load', function() {
		firstSymbolId = findFirstLayer();

		currentHeatmapId = heatmapIds[0];

		addGeoJSONSource(heatmapIds[0], GeoJSONdata);
		addGeoJSONSource(heatmapIds[1], '/frontend/assets/null.geojson');

		addGeoJSONLayer(heatmapIds[0], 'visible', minStop, maxStop);
		addGeoJSONLayer(heatmapIds[1], 'none', minStop, maxStop);

		setHeatmapColorScale(colorScheme, minStop, maxStop);
	})
}

function setHeatmap(heatmapId, GeoJSONdata) {
	map.getSource(heatmapId).setData(GeoJSONdata);
}

function setHeatmapColorScale(colorScale, minStop, maxStop) {
	var fillColor = {
		property: 'probability',
		stops: generateColorScale(colorScale, minStop, maxStop)
	};

	heatmapIds.forEach(heatmapId => {
		map.setPaintProperty(heatmapId, 'fill-color', fillColor);
	});
}

function* range(start, end, step) {
	while (start < end) {
		yield start;
		start += step;
	}
}

function generateColorScale(colorScheme, minStop, maxStop) {
	var stops = Array.from(range(minStop, maxStop, 1));
	var colors = chroma.scale(colorScheme).colors(stops.length);
	var colorScale = [];

	colors.forEach(
		(color, index) => {
			colorScale[index] = [stops[index], color]
		}
	);

	return colorScale;
}
