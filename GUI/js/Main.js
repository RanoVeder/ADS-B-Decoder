var map
var markers = []
var counter = 0
var list = {}
google.maps.event.addDomListener(window, 'load', Init_Map);

$(document).ready(function(){

    $(document).on('click', '.aircraft', function() {
      id = $(this).attr('id');
      console.log(id)
      for(var i in list){
        if(list[i] == id){
            var result = $.grep(markers, function(e){ return e.key == i; });
            if(result == 0){
              return;
            }else{
              map.setZoom(12);
              map.panTo(result[0].value.position);
              $('.aircraft').removeClass("selected")
              $(this).addClass("selected")
            }

        }

      }
      
    
});


  });

function Init_Map(){

// When the window has finished loading create our google map below


        // Basic options for a simple Google Map
        // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
        var mapOptions = {
            // How zoomed in you want the map to start at (always required)
            zoom: 8,

            // The latitude and longitude to center the map (always required)
            center: new google.maps.LatLng(52.3700, 5),
            disableDefaultUI: true,
            zoomControl: true, 

/*            styles: [ { "featureType": "all", "elementType": "labels.text.fill", "stylers": [ { "saturation": 36 }, { "color": "#000000" }, { "lightness": 40 } ] }, { "featureType": "all", "elementType": "labels.text.stroke", "stylers": [ { "visibility": "on" }, { "color": "#000000" }, { "lightness": 16 } ] }, { "featureType": "all", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "administrative", "elementType": "geometry.fill", "stylers": [ { "color": "#000000" }, { "lightness": 20 } ] }, { "featureType": "administrative", "elementType": "geometry.stroke", "stylers": [ { "color": "#000000" }, { "lightness": 17 }, { "weight": 1.2 } ] }, { "featureType": "administrative.country", "elementType": "all", "stylers": [ { "visibility": "on" } ] }, { "featureType": "administrative.country", "elementType": "geometry.fill", "stylers": [ { "visibility": "on" } ] }, { "featureType": "administrative.country", "elementType": "geometry.stroke", "stylers": [ { "color": "#1abc9c" } ] }, { "featureType": "administrative.province", "elementType": "geometry.stroke", "stylers": [ { "color": "#1abc9c" }, { "visibility": "on" } ] }, { "featureType": "landscape", "elementType": "geometry", "stylers": [ { "color": "#000000" }, { "lightness": 20 } ] }, { "featureType": "poi", "elementType": "geometry", "stylers": [ { "color": "#000000" }, { "lightness": 21 } ] }, { "featureType": "road.highway", "elementType": "all", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "geometry.fill", "stylers": [ { "color": "#000000" }, { "lightness": 17 } ] }, { "featureType": "road.highway", "elementType": "geometry.stroke", "stylers": [ { "color": "#000000" }, { "lightness": 29 }, { "weight": 0.2 } ] }, { "featureType": "road.arterial", "elementType": "geometry", "stylers": [ { "color": "#000000" }, { "lightness": 18 } ] }, { "featureType": "road.local", "elementType": "geometry", "stylers": [ { "color": "#000000" }, { "lightness": 16 } ] }, { "featureType": "transit", "elementType": "geometry", "stylers": [ { "color": "#000000" }, { "lightness": 19 } ] }, { "featureType": "water", "elementType": "geometry", "stylers": [ { "color": "#000000" }, { "lightness": 17 } ] } ]
*/        };

        // Get the HTML DOM element that will contain your map 
        // We are using a div with id="map" seen below in the <body>
        var mapElement = document.getElementById('map');

        // Create the Google Map using our element and options defined above
        map = new google.maps.Map(mapElement, mapOptions);


}




var SeenPlanes = []
setInterval(function() {
$.getJSON('../data/planes.json', function(data) {
    
    	console.log(markers);


        for(var i =0; i < data.length; i++){
        	console.log(data[i].ICAO24)
        	if(SeenPlanes.indexOf(data[i].ICAO24) == -1){
        		SeenPlanes.push(data[i].ICAO24);
        		Add_Plane(data[i]);
        	}else{
        		Update_Plane(data[i])
        	}


        }

       });
    }, 2000);


/*function Plane(json){

	this.ICAO24 = 
	this.ICAO = 
	this.ALT = 
	this.Speed = 
	this.Heading = 
	this.Lat = 
	this.Lon =

}*/

function Add_Plane(str){

  html = '<div class="aircraft" id="'+counter+'"><div class="aircraft_info"><span class="ICAO">' +str.ICAO + '</span><span class="ALT">Altidude: '+str.ALT+' ft</span><span class="Speed">Speed: ' +str.Speed+' knts</span></div></div>'      
   	$('.aircraft_container').append(html);
   	if(str.Lat != 0  && str.Lon !=0){
   		Add_Marker(str);
  }
    list[str.ICAO24] = counter;
    counter++;
    console.log(list)
}

function Update_Plane(str){
  if($('#'+list[str.ICAO24]).hasClass('selected')){
	 html = '<div class="aircraft selected" id="'+list[str.ICAO24]+'"><div class="aircraft_info"><span class="ICAO">' +str.ICAO + '</span><span class="ALT">Altidude: '+str.ALT+' ft</span><span class="Speed">Speed: ' +str.Speed+' knts</span></div></div>'      
	}else{
   html = '<div class="aircraft" id="'+list[str.ICAO24]+'"><div class="aircraft_info"><span class="ICAO">' +str.ICAO + '</span><span class="ALT">Altidude: '+str.ALT+' ft</span><span class="Speed">Speed: ' +str.Speed+' knts</span></div></div>'      
  }
  $('#'+list[str.ICAO24]).replaceWith(html);
	if(str.Lat != 0  && str.Lon !=0){
   		Update_Marker(str);
	}

}




function Icon(str){
  var icon = {

    /*url: '../img/airplane2.svg',*/
    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
    scale: 5,
    strokeColor: "#1abc9c",
    rotation: str.Heading
  }
  return icon
}


function Add_Marker(str) {

  iconn = Icon(str)

  var marker = new google.maps.Marker({
    position: new google.maps.LatLng(str.Lat,str.Lon),
    icon: iconn,
    map: map,
    title: str.ICAO,
  });

  marker.addListener('click', function(e) {
    alert('test')
  });
  markers.push({key: str.ICAO24,
  				value: marker
  				});



}




function Update_Marker(str){
    iconn = Icon(str);

	  var latlng = new google.maps.LatLng(str.Lat,str.Lon);
    var result = $.grep(markers, function(e){ return e.key == str.ICAO24; });
    console.log(result)
    if(result.length == 0){
    	Add_Marker(str);
    }else{

    	result[0].value.setPosition(latlng);
    	/*result[0].value.setTitle(str.ICAO);*/
   	  result[0].value.setIcon(iconn);
      result[0].value.setTitle(str.ICAO);
    }
}
