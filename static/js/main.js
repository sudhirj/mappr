google.load("maps", "2");
google.load("jquery", "1.2");
google.load("jqueryui", "1");

var Map = function(){
    var mapDivName;
    var map;
    var adsManager;

    return {
        initialize: function(divName,o){
            var defaults = {
                lat:0,
                lon:0,
                zoom:6
            }
            var o = $.extend(defaults, o || {});
            if (google.loader.ClientLocation && o.lat == 0 && o.lon == 0) {o.lat = google.loader.ClientLocation.latitude; o.lon = google.loader.ClientLocation.longitude;o.zoom=12}
            if (!GBrowserIsCompatible()) {alert("Sorry, this site cannot run on your browser."); return;}
            this.map = new google.maps.Map2(document.getElementById(divName));
            this.map.setCenter(new GLatLng(o.lat, o.lon), o.zoom);
            this.map.enableGoogleBar();
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
            if (o.point == null) marker = new google.maps.Marker(new google.maps.LatLng(o.lat,o.lng));
            else marker = new google.maps.Marker(o.point,{draggable:o.draggable});
            this.map.addOverlay(marker);
            return marker;
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

var Message = function(){
    return {
        show: function(o){
            var defaults = {
                msg: ""
            }
            var o = $.extend(defaults, o || {});
            body = $('body');
            msgbox = $('#info-message');
            var bh = body.height(); var bw = body.width();
            msgbox.html(o.msg).show();
            var bottom = (1/8*bh)+'px'; var left = ((bw-msgbox.outerWidth())/2);
            msgbox.css({bottom:bottom , left: left});
        },
        hide: function(){
            $('#info-message').hide();
        }
    };
}
();

var PointMaker = function(){
    var marker = null;
    var dialog = null;
    var open = false;
    return {
        initialize: function(){
            if (this.open) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-add-point').show().dialog({
                    autoOpen:false,
                    draggable:true,
                    resizable:false,
                    close: function(){PointMaker.cancel();},
                    title: "Add a Pinn",
                    show:'drop',
                    hide:'drop'
                });

                $('.ok.button',this.dialog).click(function() {PointMaker.save()});
                $('.cancel.button',this.dialog).click(function(){PointMaker.dialog.dialog('close')})


            }
            this.dialog.dialog("open");
            var center = Map.map.getCenter();
            this.marker = Map.addMarker({point:center,draggable:true});
            this.open = true;
        },
        cancel: function(){
            Map.map.removeOverlay(PointMaker.marker);
            PointMaker.marker = null;
            this.open = false;
        },
        save: function(){
            var title = $('input#text-title',PointMaker.dialog).val();
            $.post('/',{
                title: title,
                lat: PointMaker.marker.getLatLng().lat(),
                lon: PointMaker.marker.getLatLng().lng()
            });
        }
    };
}
();

var FirstTime = function(){
    var dialog = null;
    var open = false;
    return {
        initialize: function(){
            if (this.open) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-create-user').show().dialog({
                    autoOpen:false,
                    draggable:true,
                    resizable:false,
                    close: function(){FirstTime.cancel();},
                    title: "Create a PinnSpot",
                    show:'drop',
                    hide:'drop'
                });
                $('.ok.button',this.dialog).click(function() {FirstTime.save()});
                $('.cancel.button',this.dialog).click(function(){FirstTime.dialog.dialog('close')})
            }
            this.dialog.dialog("open");
            this.open = true;
        },
        cancel: function(){
            this.open = false;
        },
        save: function(){
            var url = $('input#text-url',FirstTime.dialog).val();
            $.post('/',{url: url});
        }
    };
}
();





google.setOnLoadCallback(function(){
    Map.initialize("map");
    $(document).ready(function() {
        $('#add-point').click(function() {PointMaker.initialize();});
        $('#create-user').click(function() {FirstTime.initialize();});
    });

});
