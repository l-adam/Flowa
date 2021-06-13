//
//  overlays.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

// Add a MapBox source for an overlay
// Arguments:
// 		overlay – overlay object
// 		GeoJSONdata – fetched GeoJSON data
function addGeoJSONOverlay(overlay, GeoJSONdata) {
	map.addSource(overlay.id, {
		'type': 'geojson',
		'data': GeoJSONdata
	});
}

// Add a MapBox layer for an overlay
// Arguments:
// 		overlay – overlay object
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
					'Lato Regular',
					'Open Sans Semibold',
					'Arial Unicode MS Bold'
				]
			],
			'text-size': 16,
			'text-justify': 'right'
		},
		'paint': {
			'icon-color': generateColorMatch(overlay),
			'text-color': generateColorMatch(overlay),
			'text-translate': [24, -19]
		}
	});
}

// Initialize each overlay in the dataOverlays object array
function initializeMapOverlays() {
	loadAssets(); //has to be executed after the configuration was parsed

	dataOverlays.forEach(
		(dataOverlay, index) => {
			var dataOverlayOptions = {
				'index': index,
				'type': 'overlay',
				'timelineIndex': current.timelineIndex
			};

			//fetch the GeoJSON asynchronously and then wait for the map to be loaded
			parseGeoJSONZip(dataOverlayOptions).then(function(geoJSONdata) {
				map.once('load', function() {
					addGeoJSONOverlay(dataOverlay, geoJSONdata, dataOverlay.colorScheme);

					addOverlayLayer(dataOverlay);
				});
			});
		});
}

// Change the visibility of an overlay
// Arguments:
// 		index – index of the overlay
function changeMapOverlayVisibility(index) {
	var dataOverlay = current.dataOverlays[index];
	map.setLayoutProperty(dataOverlay.id, 'visibility', dataOverlay.visibility); //this is set according to the visibility property
}

// Change the source of each data overlay to the currently selected month
function changeMapOverlayTime() {
	dataOverlays.forEach(
		(dataOverlay, index) => {
			var dataOverlayOptions = {
				'index': index,
				'type': 'overlay',
				'timelineIndex': current.timelineIndex
			};

			parseGeoJSONZip(dataOverlayOptions).then(function(geoJSONdata) {
				map.getSource(dataOverlay.id).setData(geoJSONdata);
			});
		});
}
