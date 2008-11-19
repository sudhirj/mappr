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
            this.map.addControl(new google.maps.LargeMapControl(),
                                new google.maps.ControlPosition(G_ANCHOR_TOP_LEFT, 
                                new google.maps.Size(20,150)));

            this.map.enableScrollWheelZoom();
            this.map.enableContinuousZoom();

            google.maps.Event.addListener(this.map,'click',function(overlay,  latlng,  overlaylatlng){
                if (overlay == null)
                {
                    $(Map).trigger('mapClick',{point:latlng})
                }
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
    ();var FirstTime = function(){
    var dialog = null;
    var open = false;
    var currentValue;
    return {
        initialize: function(url){
            if (!url) url = '';
            if (this.open) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-create-user').show().dialog({
                    autoOpen:false,
                    draggable:true,
                    resizable:false,
                    close: function(){FirstTime.cancel();},
                    title: "Create a PinnSpot"
                });
                FirstTime.ready();
                $('#text-url').keyup(function(e){
                    if (e.keyCode == 13) FirstTime.save();
                    else{
                        currentValue = $('#text-url').val();
                        $.get('/_check/url/'+currentValue,null,function(data,status){
                            if (data == 'Y') FirstTime.ready();
                            else FirstTime.notReady();
                        },"text");                     
                    } 
                });
                $('#text-url').keypress(function(e){
                    if(e.which == 13 || e.which == 8 || e.which == 0) return true;
                    if(48 <= e.which && e.which <= 57) return true;
                    if(65 <= e.which && e.which <= 90) return true;
                    if(97 <= e.which && e.which <= 122) return true;
                    return false;                 
                });
            }
            $('.error',this.dialog).text('');
            $('input#text-url',this.dialog).val(url);
            $('#dynamic-url').text(url);
            this.dialog.dialog("open");
            $('input#text-url',this.dialog)[0].focus();
            $('#create-button').click(function(){FirstTime.save()});
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
                    FirstTime.notReady();
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
        },
        ready: function(){
            $('#text-url').addClass('green-border').removeClass('red-border');
            $('#create-button').addClass('ok').removeClass('cancel').text('Create!');   
            $('#dynamic-url').text($('#text-url').val());         
        },
        notReady: function(){
            $('#text-url').addClass('red-border').removeClass('green-border');
            $('#create-button').addClass('cancel').removeClass('ok').text('That\'s been taken :(');
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
                        var lat = $('.lat', point).text();
                        var lon = $('.lon', point).text();
                        Map.setCenter(lat,lon);
                        PointMaker.edit(key);
                    },
                    '.delete': function(e){
                        var point = $(e.target).parents('.point');
                        var key = $('.key',point).text();
                        var lat = $('.lat', point).text();
                        var lon = $('.lon', point).text();
                        Map.setCenter(lat,lon);
                        PointMaker.del(key);
                    },
                    '.point': function(e){
                        var point = $(e.target);
                        var lat = $('.lat', point).text();
                        var lon = $('.lon', point).text();
                        Map.setCenter(lat, lon);
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
            PointList.setCount();            
        },
        getPoints: function(){
            var pointArray = [];
            $('#points .point').each(function(index) {
                var point = {
                    lat: $('.lat',this).text(),
                    lon: $('.lon',this).text()
                }
                pointArray[index] = point;
            });
            return pointArray;
        },
        setCount: function(){
            var numLeft = INFO.pointCeiling - PointList.getPoints().length;
            if (numLeft > 0) $('#add-point').text('+ Add Pinn ( '+numLeft+' left )');
            else $('#add-point').text('No more Pinns :(');
            
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
        open: function(){$('#text-title')[0].focus()},
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
                $('#text-title').keyup(function(e){if (e.keyCode == 13) PointMaker.save();});
                
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
            PointList.addAllMarkers();
            
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
            if (this.isOpen) {this.dialog.dialog('close');};
            
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
    $(Map).bind('mapLoaded', function(event) {
        $('#welcome').fadeIn();
        if (INFO.auth && INFO.emptySpot && !INFO.url) FirstTime.initialize(INFO.currentUrl);
    });
    Map.initialize("map");    
    $(document).ready(function() {
        PointList.initialize();        
        $('#create-user').click(function() {FirstTime.initialize();});    
               
    });
});