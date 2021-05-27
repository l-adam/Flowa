mapboxgl.accessToken = 'pk.eyJ1IjoiczM1NzU1NiIsImEiOiJja201NTJvdnEwYjZuMm90cHNvOXllaG43In0.oPyg05LFrXhKR5Zmd_LJzQ';

var map;

function initializeMap() {
	map = new mapboxgl.Map({
		container: 'map', // container ID
		style: 'mapbox://styles/mapbox/streets-v11', // style URL
		center: [10.743942, 59.918721], // starting position
		zoom: 12, // starting zoom
		antialias: false
	});

	map.addControl(new mapboxgl.FullscreenControl(), 'top-right');

	const mapButtonFullscreen = document.getElementsByClassName("mapboxgl-ctrl-fullscreen")[0];
	mapButtonFullscreen.addEventListener("click", () => {
		setTimeout(resize, 500);
	});

	function resize() {
		map.resize(); //Make sure the map changes size after entering full screen 
	}

	var geocoder = new MapboxGeocoder({ // Initialize the map search
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

	// Add the geocoder to the map
	map.addControl(geocoder, 'top-left');
}
