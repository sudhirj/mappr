
var PointList = function(){
    return {
        update: function(){
            $('#points').load('/_points/'+INFO.currentUrl);            
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
                    }
                })
            );
        }        
    };
}
();