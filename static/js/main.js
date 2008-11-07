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
            this.map.setCenter(new GLatLng(o.lat, o.lon), o.zoom);
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
                    title: "Set a new Pinn",
                    show:'drop',
                    hide:'drop'
                });
                $('.ok.button',this.dialog).click(function() {PointMaker.save()});
                $('.cancel.button',this.dialog).click(function(){PointMaker.close();})
            }
            $('.error',this.dialog).text('');
            $('input#text-title',this.dialog).val('');
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
            if (!this.validate()) return;
            $.ajax({
                url: '/_points/',
                type: 'POST',
                data:{
                    title: title,
                    lat: PointMaker.marker.getLatLng().lat(),
                    lon: PointMaker.marker.getLatLng().lng()
                },
                dataType: 'text',
                error: function(response,status,error){
                    $('.error',this.dialog).text(response.responseText);
                },
                success: function(data){
                    PointMaker.close();
                    $('#points').load('/_points/'+INFO.currentUrl);
                    $(PointMaker).trigger('pointCreated');
                    
                }
            });
        },
        validate: function(){
            var title = $('input#text-title',this.dialog).val();
            if ($.trim(title) == '')
            {
                $('.error',this.dialog).text('You need to provide a title for this Pinn.');
                return false;
            }
            return true;
        },
        close: function(){
            PointMaker.dialog.dialog('close');
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
                $('.cancel.button',this.dialog).click(function(){FirstTime.close()})
            }
            $('.error',this.dialog).text('');
            $('input#text-url',this.dialog).val('');
            this.dialog.dialog("open");
            this.open = true;
        },
        cancel: function(){
            this.open = false;
        },
        save: function(){
            if (!this.validate()) return;
            var url = $('input#text-url',this.dialog).val();

            $.ajax({
                type: "POST",
                url: '/',
                data: {url:url},
                success: function(data){
                    FirstTime.close();
                    $(FirstTime).trigger('urlCreated');
                    window.location = '/'+$.trim(data);
                },
                dataType: "text",
                error: function(response,status,error){
                    $('.error',this.dialog).text(response.responseText);
                }                
            });
        },
        close: function(){
            this.dialog.dialog('close');
        },
        validate: function(){
            var url = $('input#text-url',this.dialog).val();
            if ($.trim(url) == '')
            {
                $('.error',this.dialog).text('You need to provide a url for your PinnSpot.');
                return false;
            }
            //TODO: add regex validation for only letters and numbers. 
            //if ()
            return true;
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
