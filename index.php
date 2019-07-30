
<!DOCTYPE html>
<html>
<head>
	
	<title>Quick Start - Leaflet</title>

	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
    
     <!-- CDN references -->
    <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/chroma-js/1.3.4/chroma.min.js"></script>
    <script src="//d3js.org/d3.v4.min.js"></script>
    <script src="//npmcdn.com/geotiff@0.3.6/dist/geotiff.js"></script> <!-- optional -->

    <!-- Plugin -->
    <script src="https://ihcantabria.github.io/Leaflet.CanvasLayer.Field/dist/leaflet.canvaslayer.field.js"></script>
	<script src="./L.KML.js"></script>

	
</head>
<body>



<div id="map" style="width: 1000px; height: 700px;"></div>
<script>

	// Make basemap
   	const map = new L.Map('map', {center: new L.LatLng(58.4, 43.0), zoom: 11})
   	, osm = new L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19
});

   	map.addLayer(osm)

   	// Load kml file
   	var rand = Math.floor(Math.random() * 100000000000);
   	fetch('assets/sigmet.kml?n='+rand)
   		  .then( res => res.text() )
   		  .then( kmltext => {

   			  	// Create new kml overlay
   			  	parser = new DOMParser();
   			  	kml = parser.parseFromString(kmltext,"text/xml");
   			  	console.log(kml)
   				const track = new L.KML(kml)
   				map.addLayer(track)

   				// Adjust map to show the kml
   				const bounds = track.getBounds()
   				map.fitBounds( bounds )

   		  })
   		  
//	d3.text('assets/data/U.asc', function(u) {
//		d3.text('assets/data/V.asc', function(v) {
//       let vf = L.VectorField.fromASCIIGrids(u, v);
//        let layer = L.canvasLayer.vectorFieldAnim(vf).addTo(map);
//        map.fitBounds(layer.getBounds());

//        layer.on('click', function(e) {
//            if (e.value !== null) {
//                let vector = e.value;
//                let v = vector.magnitude().toFixed(2);
//                let d = vector.directionTo().toFixed(0);
//                let html = (`<span>${v} m/s to ${d}&deg</span>`);
//               let popup = L.popup()
//                    .setLatLng(e.latlng)
//                    .setContent(html)
//                    .openOn(map);
//            }
//        });
        // set how the vector arrow
//        layer.options.width = 2;
//    });
//});

</script>



</body>
</html>

