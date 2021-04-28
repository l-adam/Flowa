const colorScale = ['#0000FF', '#0000FF', '#FF7700'];
const opacityScale = [0.0, 0.5, 0.5];

function initializeHeatmap(heatmapID, GeoJSONdata, minStop, middleStop, maxStop) {
	map.on('load', function() {
		var layers = map.getStyle().layers;
		// Find the index of the first symbol layer in the map style
		var firstSymbolId;

		for (var i = 0; i < layers.length; i++) {
			if (layers[i].type === 'symbol') {
				firstSymbolId = layers[i].id;
				break;
			}
		}

		// Add a data source containing GeoJSON data.
		map.addSource('heatmap', {
			'type': 'geojson',
			'data': GeoJSONdata
		});

		// Add a new layer to visualize the polygon.
		map.addLayer({
				'id': heatmapID,
				'type': 'fill',
				'source': heatmapID, // reference the data source
				'layout': {},
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
	});

}

function setHeatmap(heatmapID, GeoJSONdata) {
	map.getSource(heatmapID).setData(GeoJSONdata);
}
