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
// 1200 is the amount of timeline steps, as defined in HTML
// It should be defined as a global constant or calculated based on max-width
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

// Change the legend after user input
function layoutChangeLegend() {
	var currentLegend = timelines[current.timelineIndex].legend[current.dataSource.id];

	layoutLegend.title.textContent = current.dataSource.legend.title;
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
	popup.style.opacity = 0;

	// The transition time is 250ms. The higher delay here is to workaround a visual glitch
	// and to give the user more time to move the cursor over the popup to copy the text
	setTimeout(function() {
		// Make sure the user hasn't moved the cursor back over the popup during the transition
		if (popup.style.opacity == 0)
			popup.style.visibility = "collapse";
	}, 300)

}

//Show a popup
// Arguments:
// 		popup – a popup div
function layoutShowPopup(popup) {
	popup.style.opacity = 1;
	popup.style.visibility = "visible";
}

// Update the legend popup contents
function layoutChangeLegendPopup() {
	var popup = document.getElementById('legendPopup');

	popup.innerText = current.dataSource.legend.description;
}
