google.load("maps", "2");
google.load("jquery", "1.2");

var Map = function(){
    var mapDivName;
    var map;
    var adsManager;

    return {
        initialize: function(divName,o){
            var defaults = {
                lat:0,
                lon:0,
                zoom:12
            }
            var o = $.extend(defaults, o || {});
            if (google.loader.ClientLocation && o.lat == 0 && o.lon == 0) {o.lat = google.loader.ClientLocation.latitude; o.lon = google.loader.ClientLocation.longitude;}
            if (!GBrowserIsCompatible()) {alert("This site cannot run on your browser."); return;}
            this.map = new google.maps.Map2(document.getElementById(divName),{googleBarOptions:{showOnLoad:true}});
            this.map.setCenter(new GLatLng(o.lat, o.lon), o.zoom);
            this.map.enableScrollWheelZoom();
            this.map.enableGoogleBar();
            this.adsManager = new google.maps.AdsManager(this.map, 'pub-7898295704528692',{maxAdsOnMap:10});
            this.adsManager.enable();
        },
        addPlainMarker: function(lat, lng){
            this.map.addOverlay(new GMarker(new GLatLng(lat, lng)));
        },
        changeToNormal: function(){
            this.map.setMapType(G_SATELLITE_MAP);
        },
        changetoHybrid: function(){
            this.map.setMapType(G_HYBRID_MAP);
        }
    };
}
();

google.setOnLoadCallback(function(){
    Map.initialize("map");
    
});
