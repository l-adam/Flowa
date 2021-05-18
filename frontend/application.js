var mapSelector = [];

function initializeLayout() {
	dataSources.forEach((dataSource, index) => {
		document.getElementById("mapSelector")
			.appendChild(mapSelector[index] = document.createElement("div"))
			.classList.add("mapSelectorEntry");

		if (defaults.dataSourceIndex == index) {
			mapSelector[index].classList.replace("mapSelectorEntry", "mapSelectorEntryActive");
		}

		mapSelector[index].appendChild(document.createTextNode(dataSource.label));
		mapSelector[index].addEventListener("click", function() {
			layoutChangeDataSource(index)
		});
	});
}

function layoutChangeDataSource(index) {
	var dataSourceOptions = {
		'index': index,
		'type': 'source',
		'timelineIndex': current.timelineIndex
	};

	var geoJSONUrl = parseGeoJSONUrl(dataSourceOptions);

	current.dataSource = dataSources[index];
	changeHeatmap(geoJSONUrl, dataSources[index].minStop, dataSources[index].maxStop);
	//timelines[current.timelineIndex].legend[dataSources[index].id]
}

window.addEventListener('load', function() {
	parseConfig().then(
		function(value) {
			initializeApplication();
		}
	)
});

function initializeApplication() {
	initializeLayout();
	initializeMap();
	initializeHeatmap(dataSources[defaults.dataSourceIndex].colorScheme, -2, 2);
	map.once('load', function() {
		initializeOverlays();
	});
}
