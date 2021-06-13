//
//  application_actions.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

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

function layoutChangeStatistics() {
	Object.keys(timelines[current.timelineIndex].statistics).forEach((statistic, index) => {
		layoutStatisticsNumbers[index].textContent = timelines[current.timelineIndex].statistics[statistic];
	});
}

function layoutChangeTimeline() {
	current.timelineIndex = Math.round(timeline.value /
		(1200 / (timelines.length - 1)));
	layoutTimeline.value = Math.round(current.timelineIndex * 1200 / (timelines.length - 1));
	changeMapOverlayTime();
	layoutUpdate();
}

function layoutUpdate() {
	var dataSourceOptions = {
		'index': current.dataSourceIndex,
		'type': 'source',
		'timelineIndex': current.timelineIndex
	};

	changeHeatmap(dataSourceOptions);

	layoutChangeStatistics();
	layoutChangeLegend();
}

function layoutChangeLegend() {
	var currentLegend = timelines[current.timelineIndex].legend[current.dataSource.id];

	layoutLegend.min.textContent = currentLegend.min;
	layoutLegend.max.textContent = currentLegend.max;
}

function layoutChangeOverlays(index) {
	changeMapOverlayVisibility(index);
}
