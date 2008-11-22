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

      if (!GBrowserIsCompatible()) {alert("Sorry, this site cannot run on your browser."); return;}
      this.map = new google.maps.Map2(document.getElementById(divName));
      google.maps.Event.addListener(this.map,'load',function(){
        $(Map).trigger('mapLoaded');
      });
      this.map.setCenter(new google.maps.LatLng(o.lat, o.lon), o.zoom);
      this.adsManager = new google.maps.AdsManager(this.map, 'ca-pub-7898295704528692',{maxAdsOnMap:5});
      this.adsManager.enable();
      this.map.addControl(new google.maps.LargeMapControl(), new google.maps.ControlPosition(G_ANCHOR_TOP_LEFT, new google.maps.Size(20,150)));
      this.map.enableScrollWheelZoom();
      this.map.enableContinuousZoom();
      this.map.enableGoogleBar()

      google.maps.Event.addListener(this.map,'click',function(overlay,  latlng,  overlaylatlng){
        if (overlay) Map.map.zoomIn(overlaylatlng, true, true);
        if (overlay == null) $(Map).trigger('mapClick',{point:latlng});
      });

      new google.maps.KeyboardHandler(this.map);
      this.icon = new google.maps.Icon(G_DEFAULT_ICON);
      this.icon.image = '/static/images/pinn.png';
      this.icon.iconSize = new google.maps.Size(21,60);
      this.icon.iconAnchor = new google.maps.Point(10,55);
      this.icon.shadow = '/static/images/shadow.png';
      this.icon.shadowSize = new google.maps.Size(50,60);

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
      if (o.point == null) marker = new google.maps.Marker(new google.maps.LatLng(o.lat,o.lon),{icon:Map.icon});
      else marker = new google.maps.Marker(o.point,{draggable:o.draggable,icon:Map.icon});
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