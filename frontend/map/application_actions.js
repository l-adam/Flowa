//
//  application_actions.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

// Change the data source based on user input
// Arguments:
// 		dataSourceIndex – index of the data source passed depending
// 			on which button was clicked
function layoutChangeDataSource(dataSourceIndex) {
	if (current.dataSourceIndex != dataSourceIndex) {
		current.dataSource = dataSources[dataSourceIndex];
		current.dataSourceIndex = dataSourceIndex;

		layoutMapSelector.forEach((layoutMapSelector, index) => {
			layoutMapSelector.classList
				.add("mapSelectorEntry", "mapSelectorEntryActive");

			// Apply the appropriate style to each data source selector button
			if (index == dataSourceIndex) {
				layoutMapSelector.classList.remove("mapSelectorEntry");
			} else {
				layoutMapSelector.classList.remove("mapSelectorEntryActive");
			}
		});

		layoutUpdate();
	}
}

// Change the statistics after user input
function layoutChangeStatistics() {
	Object.keys(timelines[current.timelineIndex].statistics).forEach((statistic, index) => {
		layoutStatisticsNumbers[index].textContent = timelines[current.timelineIndex].statistics[statistic];
	});
}

// Adjust the position of the slider in the timeline based on user input
// 1200 is the amount of timeline steps
function layoutChangeTimeline() {
	current.timelineIndex = Math.round(timeline.value /
		(1200 / (timelines.length - 1)));
	layoutTimeline.value = Math.round(current.timelineIndex * 1200 / (timelines.length - 1));
	changeMapOverlayTime();
	layoutUpdate();
}

// Perform a layout update
function layoutUpdate() {
	var dataSourceOptions = {
		'index': current.dataSourceIndex,
		'type': 'source',
		'timelineIndex': current.timelineIndex
	};

	changeHeatmap(dataSourceOptions);

	layoutChangeStatistics();
	layoutChangeLegend();
	layoutChangeLegendPopup();
}

// Changethe legend after user input
function layoutChangeLegend() {
	var currentLegend = timelines[current.timelineIndex].legend[current.dataSource.id];

	layoutLegend.min.textContent = currentLegend.min;
	layoutLegend.max.textContent = currentLegend.max;
}

// Change an overlay visibility
// Arguments:
// 		index – index of a toggled overlay
function layoutChangeOverlays(index) {
	changeMapOverlayVisibility(index);
}

//Hide a popup
// Arguments:
// 		popup – a popup div
function layoutHidePopup(popup) {
	popup.style.visibility = "hidden";
}

//Show a popup
// Arguments:
// 		popup – a popup div
function layoutShowPopup(popup) {
	popup.style.visibility = "visible";
}

function layoutChangeLegendPopup() {
	document.getElementById('legendPopup')
		.innerText = current.dataSource.legend.description;
}
