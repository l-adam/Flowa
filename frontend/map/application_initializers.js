//
//  application_initializers.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

var layoutMapSelector = []; // Array containing data source selector buttons
var layoutStatisticsNumbers = []; // Numbers in the statistics pane
var layoutLegend = {}; // An object for storing the legend {min, max}
var layoutOverlays = []; // An array containing the overlay toggles
var layoutTimeline; // An object linked to the div containing the timeline

// Initialize data source selector buttons 
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

// Initialize numbers in the statistics pane
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

// Initialize the timeline
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

		// Calculate the width of the slider
		layoutTimes[index].style.width = 100 * (1 / timelines.length) + "%";
	});

	var ruleWebKit = '#timeline::-webkit-slider-thumb { width: ' + 100 * (1 / timelines.length) + '%!important}';
	var ruleMozilla = '#timeline::-moz-range-thumb { width: ' + 100 * (1 / timelines.length) + '%!important}';

	// Inserting a rule not supported by a given browser can fail 
	try {
		document.styleSheets[0].insertRule(ruleWebKit, 0);
		document.styleSheets[0].insertRule(ruleMozilla, 0);
	} catch (err) {}

	layoutTimeline = document.getElementById("timeline");

	// 1200 is the amount of timeline steps
	layoutTimeline.value = Math.round(current.timelineIndex * 1200 / (timelines.length - 1));

	layoutTimeline.onclick = function() {
		layoutChangeTimeline();
	};

	// Support for touch-based devices
	layoutTimeline.ontouchend = function() {
		// The delay is to mitigate a mobile Firefox bug
		// Without the delay the position of the slider wouldn't be set properly
		setTimeout(layoutChangeTimeline, 10);
	};
}

// Initialize the legend
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

// Initialize overlay toggles
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

// Initialize the app after the page was loaded
// This ensures that all necessary elements are present
window.addEventListener('load', function() {
	parseConfig().then(
		function(value) {
			initializeApplication();
		}
	)
});

// Initialize all the app components
function initializeApplication() {
	initializeLayoutDataSources();
	initializeLayoutStatistics();
	initializeLayoutTimeline();
	initializeLayoutLegend();
	initializeLayoutOverlays();
	initializeMap();
	initializeMapHeatmap();
	initializeMapOverlays();
}
