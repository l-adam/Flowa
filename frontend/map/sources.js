//
//  sources.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

// Add a MapBox layer for a source
// Arguments:
// 		heatmapId – id of a source and layer used for displaying heatmaps
// 		visibility – the default visibility

var opacity = 0.5; // Heatmap opacity

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

// Add a MapBox source
// Arguments:
// 		heatmapId – id of a source used for displaying heatmaps
// 		GeoJSONdata – fetched GeoJSON data
function addGeoJSONSource(heatmapId, GeoJSONdata) {
	map.addSource(heatmapId, {
		'type': 'geojson',
		'data': GeoJSONdata
	});
}

// Initialize the heatmap
function initializeMapHeatmap() {
	var dataSourceOptions = {
		'index': defaults.dataSourceIndex,
		'type': 'source',
		'timelineIndex': defaults.timelineIndex
	};

	// Set the current state based on the defaults
	current.dataSource = dataSources[dataSourceOptions.index];
	current.dataSourceIndex = dataSourceOptions.index;
	current.heatmapId = heatmapIds[0];
	current.timelineIndex = defaults.timelineIndex;

	// There are two layers used to properly handle the loading of a heatmap
	// when it's changed later
	parseGeoJSONZip(dataSourceOptions).then(function(geoJSONdata) {
		map.once('load', function() {
			firstSymbolId = findFirstLayer();

			addGeoJSONSource(heatmapIds[0], geoJSONdata);
			addGeoJSONSource(heatmapIds[1], '/frontend/assets/null.geojson'); // An empty but valid GeoJSON source 

			addSourceLayer(heatmapIds[0], 'visible');
			addSourceLayer(heatmapIds[1], 'none');

			setHeatmapColorScale(current.heatmapId);
		})
	});
}

// Change the heapmap
// Arguments:
// 		dataSourceOptions – an object with the properties:
// 			index – data source index
// 			type – 'source'
// 			timelineIndex – current timeline index
function changeHeatmap(dataSourceOptions) {
	var heatmapOff;
	var heatmapOn;
	var minStop = current.dataSource.minStop;
	var maxStop = current.dataSource.maxStop;

	// Swap the currently used heatmap layer
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

		switchHeatmapVisibility(heatmapOff, heatmapOn);
	});
}

// Switch the visible heatmap
// Arguments:
// 		heatmapOff – the heatmap to be hidden
// 		heatmapOn – the heatmap to be shown
function switchHeatmapVisibility(heatmapOff, heatmapOn) {
	map.setLayoutProperty(heatmapOff, 'visibility', 'none');
	map.setLayoutProperty(heatmapOn, 'visibility', 'visible');
}

// Set the new data to a heatmap
// Arguments:
// 		heatmapId – id of a source used for displaying heatmaps
// 		GeoJSONdata – fetched GeoJSON data
function setHeatmap(heatmapId, GeoJSONdata) {
	map.getSource(heatmapId).setData(GeoJSONdata);
}

// Set the proper color scheme for a heatmap
// 		heatmapId – id of a source used for displaying heatmaps
function setHeatmapColorScale(heatmapId) {
	var fillColor = {
		property: current.dataSource.analyzedProperty,
		stops: generateColorScale(current.dataSource.colorScheme,
			current.dataSource.minStop, current.dataSource.maxStop)
	};

	map.setPaintProperty(heatmapId, 'fill-color', fillColor);
}
