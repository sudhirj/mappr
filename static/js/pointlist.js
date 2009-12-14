var PointList = function(){
  var pointList = $('#points');
  return {
    update: function(){
      pointList.load('/_points/'+INFO.currentUrl,null,PointList.addAllMarkers);    
    },
    extractData: function(point){
      point = $(point);
      return {
        key: $('.key',point).text(),
        lat: $('.lat',point).text(),
        lon: $('.lon',point).text()
      };        
    },
    initialize: function(){
      $('#add_point').click(function() {
        if (INFO.pointCeiling > PointList.getPoints().length) PointMaker.create();
      });
      pointList.click(
        $.delegate({
          '.edit': function(e){
            var point = PointList.extractData($(e.target).parents('.point'));
            Map.setCenter(point.lat,point.lon);
            PointMaker.edit(point.key);
          },
          '.delete': function(e){
            var point = PointList.extractData($(e.target).parents('.point'));
            Map.setCenter(point.lat,point.lon);
            PointMaker.del(point.key);
          },
          '.point': function(e){
            var point = PointList.extractData($(e.target));
            Map.setCenter(point.lat, point.lon);
          },
          '.title': function(e){
            var point = PointList.extractData($(e.target).parents('.point'));
            Map.setCenter(point.lat, point.lon);
          }
        })
      );
      PointList.addAllMarkers();
    },
    addAllMarkers: function(){
      Map.clearAllMarkers();
      pointList.find('.point').each(function(index) {
        var point = PointList.extractData($(this));
        Map.addMarker({point: Map.newPoint(point.lat, point.lon)});                
      });
      PointList.setCount();           
    },
    getPoints: function(){
      var pointArray = [];
      pointList.find('.point').each(function(index) {
        var point = PointList.extractData($(this));
        pointArray[index] = point;
      });
      return pointArray;
    },
    setCount: function(){
      var numLeft = INFO.pointCeiling - PointList.getPoints().length;
      if (numLeft > 0) $('#add_point').text('Add Pinn ( '+numLeft+' left )');
      else $('#add_point').text('No more Pinns :(');
    }        
  };
}
();