google.load("maps", "2");
google.load("jquery", "1.2");
google.load("jqueryui", "1.5");

function setUpViewShifter(){
  $(document).ready(function() {
    $("#view_shift").toggle(function() {
      $(this).removeClass('satellite_view').text('Map View').addClass('map_view');
      Map.changeToHybrid();
    }, function() {
      $(this).removeClass('map_view').text('Satellite View').addClass('satellite_view');
      Map.changeToNormal();
    });
  });  
}

google.setOnLoadCallback(function(){    
  $.delegate = function(rules) {
    return function(e) {
      var target = $(e.target);
      for (var selector in rules)
      if (target.is(selector)) return rules[selector].apply(this, $.makeArray(arguments));
    }
  };
  $(Map).bind('mapLoaded', function(event) {
    $('#load-message').fadeOut();
    var showWelcome = true;
    if ((INFO.url == INFO.currentUrl) && PointList.getPoints().length > 0) showWelcome = false;
    if (showWelcome) $('#welcome').fadeIn();
    if (INFO.auth && INFO.emptySpot && !INFO.url) FirstTime.initialize(INFO.currentUrl);
    setUpViewShifter();    
  });
  Map.initialize("map");    
  $(document).ready(function() {
    PointList.initialize();        
    $('#create_user').click(function() {FirstTime.initialize()});
    $('body').click(function(e){
      if ($(e.target).hasClass('close_button')) $(e.target).parent().fadeOut();
    });
  });
});