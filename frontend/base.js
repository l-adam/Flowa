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

function changeHeatmap(dataSourceOptions) {
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

	parseGeoJSONZip(dataSourceOptions).then(function(GeoJSONdata) {
		setHeatmap(heatmapOn, GeoJSONdata);

		setHeatmapColorScale(heatmapOn);

		map.once('idle', function() {
			switchHeatmapVisibility(heatmapOff, heatmapOn);
		});
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

		current.dataSource = dataSources[dataSourceOptions.index];
		current.dataSourceIndex = dataSourceOptions.index;
		current.heatmapId = heatmapIds[0];
		current.timelineIndex = defaults.timelineIndex;

		parseGeoJSONZip(dataSourceOptions).then(function(geoJSONdata) {
			addGeoJSONSource(heatmapIds[0], geoJSONdata);
			addGeoJSONSource(heatmapIds[1], '/frontend/assets/null.geojson');

			addSourceLayer(heatmapIds[0], 'visible');
			addSourceLayer(heatmapIds[1], 'none');

			setHeatmapColorScale(current.heatmapId);
		});
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
	var iconProperties = getIconProperties(overlay.id);

	map.addLayer({
		'id': overlay.id,
		'type': 'symbol',
		'source': overlay.id,
		'layout': {
			'icon-allow-overlap': true,
			'icon-image': iconProperties.id,
			'icon-size': iconProperties.size,
			'icon-anchor': 'bottom',
			'visibility': overlay.defaultVisibility,
			'text-allow-overlap': true,
			'text-field': ['get', overlay.analyzedProperty],
			'text-font': [
				'literal', [
					'Lato Bold',
					'Open Sans Semibold',
					'Arial Unicode MS Bold'
				]
			],
			'text-offset': [0.25, -3.25],
			'text-size': 28,
			'text-variable-anchor': ['bottom-left']

		},
		'paint': {
			'icon-color': generateColorMatch(overlay),
			'text-color': generateColorMatch(overlay),
			'text-halo-color': 'black',
			'text-halo-width': 1,
			'text-halo-blur': 4
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

function getIconProperties(id) {
	var iconProperties = {};

	assetsConfig.mapAssets.overlayIcons.forEach((overlayIcon) => {
		if (overlayIcon.id == id) {
			iconProperties.id = overlayIcon.id;
			iconProperties.size = overlayIcon.size;
			return iconProperties;
		}
	});

	if (!iconProperties.hasOwnProperty('id')) {
		iconProperties.id = assetsConfig.mapAssets.defaults.overlayIcons.id;
		iconProperties.size = assetsConfig.mapAssets.defaults.overlayIcons.size;
	}

	return iconProperties;
}

function initializeMapOverlays() {
	map.once('load', function() {
		loadAssets();

		dataOverlays.forEach(
			(dataOverlay, index) => {
				var dataOverlayOptions = {
					'index': index,
					'type': 'overlay',
					'timelineIndex': defaults.timelineIndex
				};

				parseGeoJSONUrl(dataOverlayOptions).then(function(geoJSONdata) {
					addGeoJSONOverlay(dataOverlay, geoJSONdata, dataOverlay.colorScheme);

					addOverlayLayer(dataOverlay);
				});
			});
	})
}

function changeMapOverlayVisibility(index) {
	var dataOverlay = current.dataOverlays[index];
	map.setLayoutProperty(dataOverlay.id, 'visibility', dataOverlay.visibility);
}

function changeMapOverlayTime() {
	dataOverlays.forEach(
		(dataOverlay, index) => {
			var dataOverlayOptions = {
				'index': index,
				'type': 'overlay',
				'timelineIndex': current.timelineIndex
			};

			parseGeoJSONUrl(dataOverlayOptions).then(function(geoJSONdata) {
				map.getSource(dataOverlay.id).setData(geoJSONdata);
			});
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
						'sdf': false //change to true to enable native coloring
					});
				});
		});
}
