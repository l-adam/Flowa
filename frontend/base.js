const defaultColorScheme = ['#0000FF', '#FF7700'];
const opacity = 0.5;

var current = {};
var firstSymbolId;
var heatmapIds = ['heatmap', 'heatmap2'];
var iconProperties;

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
	var minStop = current.dataSource.minStop;
	var maxStop = current.dataSource.maxStop;

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

	setHeatmapColorScale(heatmapOn);

	map.once('idle', function() {
		switchHeatmapVisibility(heatmapOff, heatmapOn);
	});
}

function switchHeatmapVisibility(heatmapOff, heatmapOn) {
	map.setLayoutProperty(heatmapOff, 'visibility', 'none');
	map.setLayoutProperty(heatmapOn, 'visibility', 'visible');
}

function addSourceLayer(heatmapId, visibility) {
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

function initializeMapHeatmap(colorScheme) {
	map.once('load', function() {
		var dataSourceOptions = {
			'index': defaults.dataSourceIndex,
			'type': 'source',
			'timelineIndex': defaults.timelineIndex
		};

		firstSymbolId = findFirstLayer();

		var geoJSONUrl = parseGeoJSONUrl(dataSourceOptions);

		current.dataSource = dataSources[dataSourceOptions.index];
		current.dataSourceIndex = dataSourceOptions.index;
		current.heatmapId = heatmapIds[0];
		current.timelineIndex = defaults.timelineIndex;

		addGeoJSONSource(heatmapIds[0], geoJSONUrl);
		addGeoJSONSource(heatmapIds[1], '/frontend/assets/null.geojson');

		addSourceLayer(heatmapIds[0], 'visible');
		addSourceLayer(heatmapIds[1], 'none');

		setHeatmapColorScale(current.heatmapId);
	})
}

function setHeatmap(heatmapId, GeoJSONdata) {
	map.getSource(heatmapId).setData(GeoJSONdata);
}

function setHeatmapColorScale(heatmapId) {
	var fillColor = {
		property: current.dataSource.analyzedProperty,
		stops: generateColorScale(current.dataSource.colorScheme,
			current.dataSource.minStop, current.dataSource.maxStop)
	};

	map.setPaintProperty(heatmapId, 'fill-color', fillColor);

	current.colorScheme = current.dataSource.colorScheme;
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

function addGeoJSONOverlay(overlay, GeoJSONdata) {
	map.addSource(overlay.id, {
		'type': 'geojson',
		'data': GeoJSONdata
	});
}

function addOverlayLayer(overlay) {
	map.addLayer({
		'id': overlay.id,
		'type': 'symbol',
		'source': overlay.id,
		'layout': {
			'icon-allow-overlap': true,
			'icon-image': iconProperties.ids,
			'icon-size': iconProperties.sizes,
			'visibility': overlay.defaultVisibility,
			'text-allow-overlap': true,
			'text-field': ['get', overlay.analyzedProperty],
			'text-font': [
				'Open Sans Semibold',
				'Arial Unicode MS Bold'
			],
			'text-offset': [0, 1.25],
			'text-anchor': 'top'
		},
		'paint': {
			'icon-color': generateColorMatch(overlay)
		}
	});
}

function generateColorMatch(overlay) {
	var stops = Array.from(range(overlay.minStop, overlay.maxStop, 1));
	var colors = chroma.scale(overlay.colorScheme).colors(stops.length);
	var colorMatch = ['match', ['get', overlay.analyzedProperty]];

	colors.forEach(
		(color, index) => {
			colorMatch.push(stops[index], color);
		}
	);

	colorMatch.push('#FF0000');

	return colorMatch;
}

function generateIconProperties() {
	iconProperties = {};

	iconProperties.ids = ['match', ['get', 'id']];
	iconProperties.sizes = ['match', ['get', 'id']];

	assetsConfig.mapAssets.overlayIcons.forEach(
		(icon, index) => {
			iconProperties.ids.push(icon.id, icon.id);
			iconProperties.sizes.push(icon.id, icon.size);
		}
	);

	iconProperties.ids.push(assetsConfig.mapAssets.defaults.overlayIcons.id);
	iconProperties.sizes.push(assetsConfig.mapAssets.defaults.overlayIcons.size);
}

function initializeMapOverlays() {
	map.once('load', function() {
		loadAssets();
		generateIconProperties();

		dataOverlays.forEach(
			(dataOverlay, index) => {
				var dataOverlayOptions = {
					'index': index,
					'type': 'overlay',
					'timelineIndex': defaults.timelineIndex
				};

				addGeoJSONOverlay(dataOverlay,
					parseGeoJSONUrl(dataOverlayOptions), dataOverlay.colorScheme);

				addOverlayLayer(dataOverlay);
			});
	})
}

function changeMapOverlay(index) {
	var dataOverlay = current.dataOverlays[index];
	map.setLayoutProperty(dataOverlay.id, 'visibility', dataOverlay.visibility);
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
