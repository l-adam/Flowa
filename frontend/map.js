//
//  map.js
//  Flowa
//
//  Created by Adam Lewczuk.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

mapboxgl.accessToken = 'pk.eyJ1IjoiczM1NzU1NiIsImEiOiJja201NTJvdnEwYjZuMm90cHNvOXllaG43In0.oPyg05LFrXhKR5Zmd_LJzQ';

var map;

function initializeMap() {
	map = new mapboxgl.Map({
		container: 'map', // ontainer ID
		style: 'mapbox://styles/mapbox/streets-v11', // style URL
		center: [10.743942, 59.918721], // starting position
		zoom: 12, // starting zoom
		antialias: false // prevents visible edge boundaries
	});

	// Make sure the map changes size after entering full screen 
	function resize() {
		setTimeout(function() {
			map.resize();
		}, 500); // Most animations of entering full screen are less than 500 ms
	}

	// Initialize the map search
	var geocoder = new MapboxGeocoder({
		accessToken: mapboxgl.accessToken, // Set the access token
		mapboxgl: mapboxgl, // Set the mapbox-gl instance
		marker: false, // Do not use the default marker style
		placeholder: 'Search', // Placeholder text for the search bar
		bbox: [10.343942, 59.118721, 11.343942, 60.918721], // Boundaries of Oslo
		proximity: {
			longitude: 10.7439428,
			latitude: 59.918721
		}
	});

	map.addControl(geocoder, 'top-left'); // Add the map search box
	map.addControl(new mapboxgl.FullscreenControl(), 'top-right');

	// Verify if the fullscreen button was successfully created
	// On some mobile platforms fullscreen is not supported
	const mapButtonFullscreen = document.getElementsByClassName("mapboxgl-ctrl-fullscreen")[0];
	if (typeof mapButtonFullscreen != 'undefined') {
		mapButtonFullscreen.addEventListener("click", () => {
			resize();
		});
	}
}
