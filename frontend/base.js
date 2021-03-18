//const probabilityRangeMax = 255;
//var colorScale = ['#0000ff00','blue','cyan','green','yellow','red'];
const probabilityRangeMax = 22;
const colorScale = ['green','red'];

var probabilityPossibleValues = Array.from(Array(probabilityRangeMax + 1), (_,x) => x);;

function getColorChroma(n,classBreaks,colorHex) {
    var mapScale = chroma.scale(colorHex).classes(classBreaks);
    if (n === 0) {
        var regionColor = '#ffffff';
    } else { 
        var regionColor = mapScale(n).hex();
    }
    return regionColor
}

function heatmap(feature) {
    return {
        fillColor: getColorChroma(feature.properties.completeness,probabilityPossibleValues,colorScale),
        weight: 0,
        opacity: 1,
        fillOpacity: 0.7
    };
}

function geoJSONadd(geoJSONsource) {
	return new L.GeoJSON.AJAX(geoJSONsource, {style: heatmap}).addTo(map);
}
