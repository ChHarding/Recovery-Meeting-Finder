var map = L.map('map').setView([42.0308, -93.6319],15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 10,
    attribution: ''
}).addTo(map);

var searchControl = new L.esri.Controls.Geosearch().addTo(map);

var results = new L.LayerGroup().addTo(map);

  searchControl.on('results', function(data){
    results.clearLayers();
    for (var i = data.results.length - 1; i >= 0; i--) {
      results.addLayer(L.marker(data.results[i].latlng));
    }
  });

searchBox = document.getElementsByClassName('geocoder-control leaflet-control')[0];
searchBox.style.width=423;
searchBox.style.position='fixed';
searchBox.style.float='right';
searchBox.style.right='55px';
searchBox.style.top='80px';

searchBoxInput = document.getElementsByClassName('geocoder-control-input leaflet-bar')[0];
searchBoxInput.style.height='40px';
searchBoxInput.style.borderRadius='10px';

// -- Get user's location --------------------------------------

var currentLocIcon = L.icon({
    iconUrl: 'img/cur_loc.png',
    //iconSize:     [20, 20], // size of the icon
});


map.locate({setView: true, watch: true}) // This will return map so you can do chaining
        .on('locationfound', function(e){
            var currentLocMarker = L.marker([e.latitude, e.longitude], {iconUrl: currentLocIcon}).bindPopup('Your are here :)');
            currentLocMarker.setIcon(currentLocIcon);
            map.addLayer(currentLocMarker);
            map.setZoom(5);

        })
       .on('locationerror', function(e){
            console.log(e);
            alert("User's location access denied.");
        });

map.setZoom(5);





// -- Get JSON data of meetings ---------------------------------
y12sr = JSON.parse(correct_json(YData));
smart = JSON.parse(correct_json(SData));

console.log(y12sr.length.toString() + " records are loaded for Y12SR meetings.");
console.log(smart.length.toString() + " records are loaded for SMART meetings.");


// -- Show the markers ---------------------------------
refreshMap();
