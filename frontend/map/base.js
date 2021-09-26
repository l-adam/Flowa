//
//  base.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

var current = {}; //data structure for storing the current state of the map
var firstSymbolId; // The index of the first symbol layer in the map style
var heatmapIds = ['heatmap', 'heatmap2']; //layers used to display heatmaps

// Find the index of the first symbol layer in the map style
// This is to display a MapBox source below other map elements (e.g. streets)
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

// Generate a color value for each possible property value
// Arguments:
// 		colorScheme – an array containing RGB values to be used in the gradient
// 		minStop – minimum value of an examined property
// 		maxStop – maximum value of an examined property
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

// Generate a MapBox expression with the color scheme of an overlay
// for each of the possible property values
// Arguments:
// 		overlay – overlay object
function generateColorMatch(overlay) {
	var stops = Array.from(range(overlay.minStop, overlay.maxStop, 1));
	var colors = chroma.scale(overlay.colorScheme).colors(stops.length);
	var colorMatch = ['match', ['get', overlay.analyzedProperty]];

	colors.forEach(
		(color, index) => {
			colorMatch.push(stops[index], color);
		}
	);

	// Color value for properties outside of the specified range
	colorMatch.push(colors[colors.length - 1]);

	return colorMatch;
}

// A helper function to generate values in the given range
function* range(start, end, step) {
	while (start < end) {
		yield start;
		start += step;
	}
}

// Get icon properties for a given overlay id
// 		id – overlay id
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

// Load overlay icons
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
