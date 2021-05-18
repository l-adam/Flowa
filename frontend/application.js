var layoutMapSelector = [];
var layoutStatisticsNumbers = [];

function initializeLayoutDataSources() {
	dataSources.forEach((dataSource, index) => {
		document.getElementById("mapSelector")
			.appendChild(layoutMapSelector[index] = document.createElement("div"))
			.classList.add("mapSelectorEntry");

		if (defaults.dataSourceIndex == index) {
			layoutMapSelector[index].classList
				.replace("mapSelectorEntry", "mapSelectorEntryActive");
		}

		layoutMapSelector[index].appendChild(document.createTextNode(dataSource.label));
		layoutMapSelector[index].addEventListener("click", function() {
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

	layoutMapSelector.forEach((layoutMapSelector, index) => {
		layoutMapSelector.classList
			.add("mapSelectorEntry", "mapSelectorEntryActive");

		if (index == dataSourceIndex) {
			layoutMapSelector.classList.remove("mapSelectorEntry");
		} else {
			layoutMapSelector.classList.remove("mapSelectorEntryActive");
		}
	});
}

function initializeLayoutStatistics() {
	Object.keys(timelines[current.timelineIndex].statistics).forEach((statistic, index) => {
		document.getElementById(statistic)
			.appendChild(layoutStatisticsNumbers[index] = document.createElement("div"))
			.classList.add("statisticsNumber");

		layoutStatisticsNumbers[index].id = statistic + "Number";
		layoutStatisticsNumbers[index]
			.appendChild(document
				.createTextNode(timelines[current.timelineIndex].statistics[statistic]));
	});
}

function layoutChangeStatistics() {
	Object.keys(timelines[current.timelineIndex].statistics).forEach((statistic, index) => {
		layoutStatisticsNumbers[index].textContent = timelines[current.timelineIndex].statistics[statistic];
	});
}

function initializeLayoutTimeline() {
	var layoutTimes = [];

	timelines.forEach((time, index) => {
		var layoutMonth;
		var layoutYear;

		document.getElementById("timelineDescription")
			.appendChild(layoutTimes[index] = document.createElement("div"))
			.classList.add("time");

		layoutTimes[index].appendChild(layoutMonth = document.createElement("div"))
			.classList.add("month");
		layoutTimes[index].appendChild(layoutYear = document.createElement("div"))
			.classList.add("year");

		layoutMonth.appendChild(document.createTextNode(time.label.month));
		layoutYear.appendChild(document.createTextNode(time.label.year));

		layoutTimes[index].style.width = 100 * (1 / timelines.length) + "%"
	});
}

function initializeLayoutLegend() {
	var legendRange = {};
	var currentLegend = timelines[current.timelineIndex].legend[current.dataSource.id];

	document.getElementById("legendText")
		.appendChild(legendRange.min = document.createElement("div"));
	legendRange.min.appendChild(document.createTextNode("<" + currentLegend.min));
	legendRange.min.id = "legendMinText";

	document.getElementById("legendText")
		.appendChild(legendRange.max = document.createElement("div"));
	legendRange.max.appendChild(document.createTextNode("<" + currentLegend.max));
	legendRange.max.id = "legendMaxText";
}

window.addEventListener('load', function() {
	parseConfig().then(
		function(value) {
			initializeApplication();
		}
	)
});

function initializeApplication() {
	initializeLayoutDataSources();
	initializeLayoutStatistics();
	initializeLayoutTimeline();
	initializeLayoutLegend();
	initializeMap();
	initializeHeatmap(dataSources[defaults.dataSourceIndex].colorScheme, -2, 2);
	map.once('load', function() {
		initializeOverlays();
	});
}
