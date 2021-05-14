const defaultColorScheme = ['#0000FF', '#FF7700'];
const opacity = 0.5;

var current = {};
var firstSymbolId;
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

	if (current.heatmapId == heatmapIds[0]) {
		heatmapOff = heatmapIds[0];
		heatmapOn = heatmapIds[1]
		current.heatmapId = heatmapIds[1];
	} else {
		heatmapOff = heatmapIds[1];
		heatmapOn = heatmapIds[0]
		current.heatmapId = heatmapIds[0];
	}

	setHeatmap(heatmapOn, GeoJSONdata);

	setHeatmapColorScale(current.colorScheme, minStop, maxStop);

	map.once('data', function() {
		switchHeatmapVisibility(heatmapOff, heatmapOn);
	});
}

function switchHeatmapVisibility(heatmapOff, heatmapOn) {
	map.setLayoutProperty(heatmapOff, 'visibility', 'none');
	map.setLayoutProperty(heatmapOn, 'visibility', 'visible');
}

function addSourceLayer(heatmapId, visibility, minStop, maxStop) {
	map.addLayer({
			'id': heatmapId,
			'type': 'fill',
			'source': heatmapId,
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

function initializeHeatmap(dataSourceOptions, colorScheme, minStop, maxStop) {
	map.once('load', function() {
		firstSymbolId = findFirstLayer();

		var geoJSONUrl = parseGeoJSONUrl(dataSourceOptions);

		current.dataSource = dataSources[dataSourceOptions.index];
		current.heatmapId = heatmapIds[0];

		addGeoJSONSource(heatmapIds[0], geoJSONUrl);
		addGeoJSONSource(heatmapIds[1], '/frontend/assets/null.geojson');

		addSourceLayer(heatmapIds[0], 'visible', minStop, maxStop);
		addSourceLayer(heatmapIds[1], 'none', minStop, maxStop);

		setHeatmapColorScale(colorScheme, minStop, maxStop);
	})
}

function setHeatmap(heatmapId, GeoJSONdata) {
	map.getSource(heatmapId).setData(GeoJSONdata);
}

function setHeatmapColorScale(colorScheme, minStop, maxStop) {
	var fillColor = {
		property: current.dataSource.analyzedProperty,
		stops: generateColorScale(colorScheme, minStop, maxStop)
	};

	heatmapIds.forEach(heatmapId => {
		map.setPaintProperty(heatmapId, 'fill-color', fillColor);
	});

	current.colorScheme = colorScheme;
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

function addGeoJSONOverlay(overlayId, GeoJSONdata) {
	map.addSource(overlayId, {
		'type': 'geojson',
		'data': GeoJSONdata
	});
}

function addOverlayLayer(overlayId, visibility, minStop, maxStop) {
	map.addLayer({
		'id': overlayId,
		'type': 'symbol',
		'source': overlayId,
		'layout': {
			'icon-image': 'pin',
			'icon-size': 0.25,
			'visibility': visibility
		},
		'paint': {
			'icon-color': generateColorMatch(current.dataSource.colorScheme, minStop, maxStop)
		}
	});
}

function generateColorMatch(colorScheme, minStop, maxStop) {
	var stops = Array.from(range(minStop, maxStop, 1));
	var colors = chroma.scale(colorScheme).colors(stops.length);
	var colorMatch = ['match', ['get', 'cases_this_month']];

	colors.forEach(
		(color, index) => {
			colorMatch.push(stops[index], color);
		}
	);

	colorMatch.push('#FF0000');

	return colorMatch;
}

function initializeOverlays() {
	loadAssets();

	dataOverlays.forEach(
		(dataOverlay, index) => {
			var dataOverlayOptions = {
				'index': index,
				'type': 'overlay',
				'timelineIndex': defaults.timelineIndex
			};

			addGeoJSONOverlay(dataOverlay.id,
				parseGeoJSONUrl(dataOverlayOptions), dataOverlay.colorScheme);

			addOverlayLayer(dataOverlay.id, dataOverlay.defaultVisibility,
				dataOverlay.minStop, dataOverlay.maxStop)
		});
}

function loadAssets() {
	assetsConfig.mapAssets.overlayIcons.forEach(
		(overlayIcon, index) => {
			map.loadImage(
				overlayIcon.url,
				function(error, image) {
					if (error) throw error;
					map.addImage(overlayIcon.id, image, {
						'sdf': true
					});
				});
		});
}
