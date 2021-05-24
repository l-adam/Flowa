var layoutMapSelector = [];
var layoutStatisticsNumbers = [];
var layoutLegend = {};
var layoutOverlays = [];

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
	if (current.dataSourceIndex != dataSourceIndex) {
		current.dataSource = dataSources[dataSourceIndex];
		current.dataSourceIndex = dataSourceIndex;

		layoutMapSelector.forEach((layoutMapSelector, index) => {
			layoutMapSelector.classList
				.add("mapSelectorEntry", "mapSelectorEntryActive");

			if (index == dataSourceIndex) {
				layoutMapSelector.classList.remove("mapSelectorEntry");
			} else {
				layoutMapSelector.classList.remove("mapSelectorEntryActive");
			}
		});

		layoutUpdate();
	}
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

		layoutTimes[index].style.width = 100 * (1 / timelines.length) + "%";
	});

	var ruleWebKit = '#timeline::-webkit-slider-thumb { width: ' + 100 * (1 / timelines.length) + '%!important}';
	var ruleMozilla = '#timeline::-moz-range-thumb { width: ' + 100 * (1 / timelines.length) + '%!important}';

	try {
		document.styleSheets[0].insertRule(ruleWebKit, 0);
		document.styleSheets[0].insertRule(ruleMozilla, 0);
	} catch (err) {}

	var layoutTimeline = document.getElementById("timeline");

	layoutTimeline.value = Math.round(current.timelineIndex * 1200 / (timelines.length - 1));

	layoutTimeline.onclick = function() {
		current.timelineIndex = Math.round(timeline.value /
			(1200 / (timelines.length - 1)));
		layoutTimeline.value = Math.round(current.timelineIndex * 1200 / (timelines.length - 1));
		layoutUpdate();
	}
}

function layoutUpdate() {
	var dataSourceOptions = {
		'index': current.dataSourceIndex,
		'type': 'source',
		'timelineIndex': current.timelineIndex
	};

	var geoJSONUrl = parseGeoJSONUrl(dataSourceOptions);

	changeHeatmap(geoJSONUrl);

	layoutChangeStatistics();
	layoutChangeLegend();
}

function initializeLayoutLegend() {
	var currentLegend = timelines[current.timelineIndex].legend[current.dataSource.id];

	document.getElementById("legendText")
		.appendChild(layoutLegend.min = document.createElement("div"));
	layoutLegend.min.appendChild(document.createTextNode(currentLegend.min));
	layoutLegend.min.id = "legendMinText";

	document.getElementById("legendText")
		.appendChild(layoutLegend.max = document.createElement("div"));
	layoutLegend.max.appendChild(document.createTextNode(currentLegend.max));
	layoutLegend.max.id = "legendMaxText";
}

function layoutChangeLegend() {
	var currentLegend = timelines[current.timelineIndex].legend[current.dataSource.id];

	layoutLegend.min.textContent = currentLegend.min;
	layoutLegend.max.textContent = currentLegend.max;
}

function initializeLayoutOverlays() {
	current.dataOverlays.forEach((overlay, index) => {
		var layoutOverlayContainer;

		document.getElementById("overlays")
			.appendChild(layoutOverlayContainer = document.createElement("div"))
			.classList.add("overlay");

		var html = "<label><input type=\"checkbox\"><span>";

		layoutOverlayContainer.innerHTML = html + overlay.label + "</span></label>";
		layoutOverlays[index] = layoutOverlayContainer.getElementsByTagName("input")[0];

		layoutOverlays[index].addEventListener("click", function() {
			if (layoutOverlays[index].checked == true) {
				overlay.visibility = 'visible';
			} else {
				overlay.visibility = 'none';
			}

			layoutChangeOverlays(index);
		});

		if (overlay.defaultVisibility == 'visible') {
			layoutOverlays[index].checked = true;
		}
	});
}

function layoutChangeOverlays(index) {
	changeMapOverlay(index);
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
	initializeLayoutOverlays();
	initializeMap();
	initializeMapHeatmap();
	map.once('load', function() {
		initializeMapOverlays();
	});
}
