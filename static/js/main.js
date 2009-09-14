var ROUTES = {
  URL: {
    check: function (url){return '/_check/url/'+url;},
    create: function (url){return '/_create/'+url;}
  },
  MAIN: {
    spot: function (spot){return '/'+spot;}
  }
  
}

var EVENTS = {
  URL: {
    CREATED: 'urlCreated'
  }
}

$.delegate = function(rules) {
  return function(e) {
    var target = $(e.target);
    for (var selector in rules){
      if (target.is(selector)) return rules[selector].apply(this, $.makeArray(arguments));
    }
  }
};

$(document).ready(function() {
  $(Map).bind('mapLoaded', function(event) {
    $('#load-message').fadeOut();
    var showWelcome = ((INFO.url == INFO.currentUrl) && PointList.getPoints().length > 0);
    if (showWelcome) $('#welcome').fadeIn();
    if (INFO.auth && INFO.emptySpot && !INFO.url) FirstTime.initialize(INFO.currentUrl);
  });
  $('#create_user').click(function() {FirstTime.initialize(INFO.currentUrl)});
  $('body').click(
    $.delegate({
      '.close_button': function(e){$(e.target).parent().fadeOut();},
      '.show_help': function(e){$('#welcome').fadeIn();},
      '.show_create':function(e){FirstTime.initialize(INFO.currentUrl);}
    })
  );
  Map.initialize("map");
  PointList.initialize();        
});
