var Map = function(){
    var mapDivName;
    var map;
    var adsManager;

    return {
        initialize: function(divName,o){
            var defaults = {
                lat:0,
                lon:0,
                zoom:2
            }
            var o = $.extend(defaults, o || {});
            if (google.loader.ClientLocation && o.lat == 0 && o.lon == 0) {
                o.lat = google.loader.ClientLocation.latitude; 
                o.lon = google.loader.ClientLocation.longitude;
                o.zoom = 12
            }
            if (!GBrowserIsCompatible()) {alert("Sorry, this site cannot run on your browser."); return;}
            this.map = new google.maps.Map2(document.getElementById(divName));
            this.map.setCenter(new google.maps.LatLng(o.lat, o.lon), o.zoom);
            this.adsManager = new google.maps.AdsManager(this.map, 'ca-pub-7898295704528692',{maxAdsOnMap:10});
            this.adsManager.enable();
            this.map.addControl(new GLargeMapControl());

            this.map.enableScrollWheelZoom();
            this.map.enableContinuousZoom();

            google.maps.Event.addListener(this.map,'click',function(overlay,  latlng,  overlaylatlng){
                if (overlay == null)
                {
                    $(Map).trigger('mapClick',{point:latlng})
                }
            });
            new google.maps.KeyboardHandler(this.map);
        },
        addMarker: function(o){
            var defaults = {
                lat:0,
                lon:0,
                point: null,
                draggable:false
            }
            var o = $.extend(defaults, o || {});
            var marker;
            if (o.point == null) marker = new google.maps.Marker(new google.maps.LatLng(o.lat,o.lon));
            else marker = new google.maps.Marker(o.point,{draggable:o.draggable});
            this.map.addOverlay(marker);
            return marker;
        },
        changeToNormal: function(){
            this.map.setMapType(G_SATELLITE_MAP);
        },
        changetoHybrid: function(){
            this.map.setMapType(G_HYBRID_MAP);
        },
        removeMarker: function(marker){
            this.map.removeOverlay(marker);
        },
        newPoint: function(lat, lon){
            return new google.maps.LatLng(lat,lon);
        },
        center: function(){return this.map.getCenter()},
        examine: function(marker){return {lat: marker.getLatLng().lat(), lon: marker.getLatLng().lng()}},
        clearAllMarkers: function(){this.map.clearOverlays();},
        setCenter: function(lat, lon, zoom){
            if (!zoom) var zoom = this.map.getZoom();
            this.map.panTo(new google.maps.LatLng(lat, lon), zoom);
        }
        
    };
}
();