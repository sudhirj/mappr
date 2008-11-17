
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
        }        
    };
}
();