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
            //TODO: add regex validation to allow only letters and numbers. 
            return true;
        }
    };
}
();google.load("maps", "2");
google.load("jquery", "1.2");
google.load("jqueryui", "1.5");
google.setOnLoadCallback(function(){    
    $.delegate = function(rules) {
        return function(e) {
            var target = $(e.target);
            for (var selector in rules)
            if (target.is(selector)) return rules[selector].apply(this, $.makeArray(arguments));
        }
    };
    Map.initialize("map");    
    $(document).ready(function() {
        PointList.initialize();        
        $('#create-user').click(function() {FirstTime.initialize();});            
    });
});var Map = function(){
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
            this.map.setCenter(new google.maps.LatLng(lat, lon), zoom);
        }
        
    };
}
();var Message = function(){
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
var PointList = function(){
    return {
        update: function(){
            $('#points').load('/_points/'+INFO.currentUrl,null,PointList.addAllMarkers);    
        },
        initialize: function(){
            $('#add-point').click(function() {PointMaker.create();});
            $('#points').click(
                $.delegate({
                    '.edit': function(e){
                        var point = $(e.target).parents('.point');
                        var key = $('.key',point).text();
                        PointMaker.edit(key);
                    },
                    '.delete': function(e){
                        var point = $(e.target).parents('.point');
                        var key = $('.key',point).text();
                        PointMaker.del(key);
                    },
                    '.title': function(e){
                        var point = $(e.target).parents('.point');
                        var lat = $('.lat', point).text();
                        var lon = $('.lon', point).text();
                        Map.setCenter(lat, lon);
                    }
                })
            );
            PointList.addAllMarkers();
            
        },
        addAllMarkers: function(){
            Map.clearAllMarkers();
            $('#points .point').each(function(index) {
                var lat = $('.lat',$(this)).text();
                var lon = $('.lon',$(this)).text();
                Map.addMarker({lat:lat, lon:lon});
                
            });            
        }        
    };
}
();var PointMaker = function(){
    var marker = null;
    var dialog = null;
    var isOpen = false;
    var dialogOpts = {
        autoOpen:false,
        draggable:true,
        resizable:false,
        close: function(){PointMaker.cancel();},
        show:'drop',
        hide:'drop',
        position: [100,50]
    };
    var data = null;
    return {
        create: function(){
            if (this.isOpen) PointMaker.close();
            var center = Map.center();
            this.data = {
                dialogTitle: "Push a new Pinn",
                title: "",
                point: center
            };
            this.initialize();
            $('#text-title').val('');
        },
        edit: function(key){
            if (this.isOpen) PointMaker.close();
            var point = $('#points .point:has(.key:contains('+key+'))');
            var lat = $('.lat',point).text();
            var lon = $('.lon',point).text();
            var title = $('.title',point).text();
            var latlon = Map.newPoint(lat,lon);

            this.data = {
                dialogTitle: "Change this Pinn",
                key: key,
                point: latlon
            };          
            this.initialize();          
            $('#text-title').val(title);
        },
        del: function(key){
            var answer = confirm('Are you sure you want to delete this Pinn?');
            if (!answer) return;
            if (this.isOpen) this.close();
            $.ajax({
                url: '/_points/delete/',
                type: 'POST',
                data: {key: key},
                success: PointList.update
            });
        },
        initialize: function(){
            if (this.isOpen) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-add-point').show().dialog(dialogOpts);
                $('.ok.button',this.dialog).click(function() {PointMaker.save()});
                $('.cancel.button',this.dialog).click(function() {PointList.addAllMarkers();PointMaker.close()})
            }
            $('.error',this.dialog).text('');
            $('span.ui-dialog-title',this.dialog.parent()).text(this.data.dialogTitle);
            this.dialog.dialog("open");
            Map.clearAllMarkers();
            this.marker = Map.addMarker({point:this.data.point,draggable:true});
            this.isOpen = true;
        },
        cancel: function(){
            Map.removeMarker(PointMaker.marker);
            PointMaker.marker = null;
            this.isOpen = false;
            
        },
        save: function(){
            var title = $('input#text-title',PointMaker.dialog).val();
            if (!this.validate()) return;
            var pointData = {
                title: title,                
                lat: Map.examine(this.marker).lat,
                lon: Map.examine(this.marker).lon
            };
            if (this.data.key) $.extend(pointData,{key:this.data.key});            
            $.ajax({
                url: '/_points/',
                type: 'POST',
                data: pointData,
                dataType: 'text',
                error: function(response,status,error){
                    $('.error',this.dialog).text(response.responseText);
                },
                success: function(data){
                    PointMaker.close();
                    PointList.update();
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
            if (this.isOpen) {this.dialog.dialog('close');}
        }
    };
}
();