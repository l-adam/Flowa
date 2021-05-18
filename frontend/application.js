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

function layoutChangeDataSource(dataSourceIndex) {
	var dataSourceOptions = {
		'index': dataSourceIndex,
		'type': 'source',
		'timelineIndex': current.timelineIndex
	};

	var geoJSONUrl = parseGeoJSONUrl(dataSourceOptions);

	current.dataSource = dataSources[dataSourceIndex];
	changeHeatmap(geoJSONUrl, dataSources[dataSourceIndex].minStop,
		dataSources[dataSourceIndex].maxStop);
	//timelines[current.timelineIndex].legend[dataSources[index].id]

	mapSelector.forEach((mapSelector, index) => {
		if (index == dataSourceIndex) {
			mapSelector.classList.add("mapSelectorEntry", "mapSelectorEntryActive");
			mapSelector.classList.remove("mapSelectorEntry");
		} else {
			mapSelector.classList.add("mapSelectorEntry", "mapSelectorEntryActive");
			mapSelector.classList.remove("mapSelectorEntryActive");
		}
	});
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
