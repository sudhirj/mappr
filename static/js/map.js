var Map = function(){
    var mapDivName;
    var map;
    var adsManager;
    var icon = null;

    return {
        initialize: function(divName,o){
            var defaults = {
                lat:0,
                lon:0,
                zoom:2
            }
            var o = $.extend(defaults, o || {});
            var points = PointList.getPoints();
            if (points.length > 0) {     
                o.lat = points[0].lat;
                o.lon = points[0].lon;
                o.zoom = 12;
            }
            else if (google.loader.ClientLocation) {
                o.lat = google.loader.ClientLocation.latitude; 
                o.lon = google.loader.ClientLocation.longitude;
                o.zoom = 12;
            }

            // if (!GBrowserIsCompatible()) {alert("Sorry, this site cannot run on your browser."); return;}
            this.map = new google.maps.Map(document.getElementById(divName),{
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                zoom:o.zoom,
                center: new google.maps.LatLng(o.lat, o.lon),
                navigationControlOptions:{style: google.maps.NavigationControlStyle.DEFAULT}
            });
            google.maps.event.addListener(this.map,'load',function(){
                $(Map).trigger('mapLoaded');
            });
            this.map.set_center(new google.maps.LatLng(o.lat, o.lon), o.zoom);
            // this.adsManager = new google.maps.AdsManager(this.map, 'ca-pub-7898295704528692',{maxAdsOnMap:5});

            google.maps.event.addListener(this.map,'click',function(overlay,  latlng,  overlaylatlng){
                if (overlay) Map.map.zoomIn(overlaylatlng, true, true);
                if (overlay == null) $(Map).trigger('mapClick',{point:latlng});
            });

            
            this.marker.image = new google.maps.MarkerImage({
                url: '/static/images/pinn.png',
                anchor: new google.maps.Point(10,55),
                size: new google.maps.Size(21,60)
            });
            this.marker.shadow = new google.maps.MarkerImage({
                url: '/static/images/shadow.png',
                size: new google.maps.Size(50,60)
            });

        },
        addMarker: function(o){
            var defaults = {
                lat: o.lat,
                lon: o.lon,
                point: null,
                draggable:false
            }
            var o = $.extend(defaults, o || {});

            var marker = new google.maps.Marker(o.point,{draggable:o.draggable,icon:Map.icon});
            this.map.addOverlay(marker);
            return marker;
        },
        changeToNormal: function(){
            this.map.setMapType(G_NORMAL_MAP);
        },
        changeToHybrid: function(){
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
            this.map.panTo(new google.maps.LatLng(lat, lon));
        }

    };
}
();