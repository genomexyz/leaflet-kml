
<!DOCTYPE html>
<html>
<head>
	
	<title>Quick Start - Leaflet</title>

	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
	<script src="./L.KML.js"></script>

	
</head>
<body>



<div id="map" style="width: 600px; height: 400px;"></div>
<script>

	// Make basemap
   	const map = new L.Map('map', {center: new L.LatLng(58.4, 43.0), zoom: 11})
   	, osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')

   	map.addLayer(osm)

   	// Load kml file
   	fetch('assets/example1.kml')
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

</script>



</body>
</html>

