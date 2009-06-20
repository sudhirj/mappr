$.delegate = function(rules) {
    return function(e) {
        var target = $(e.target);
        for (var selector in rules)
        if (target.is(selector)) return rules[selector].apply(this, $.makeArray(arguments));
    }
};
$(Map).bind('mapLoaded', function(event) {
    $('#load-message').fadeOut();
    var showWelcome = ((INFO.url == INFO.currentUrl) && PointList.getPoints().length > 0);
    if (showWelcome) $('#welcome').fadeIn();
    if (INFO.auth && INFO.emptySpot && !INFO.url) FirstTime.initialize(INFO.currentUrl);
});

Map.initialize("map");    

$(document).ready(function() {
    PointList.initialize();        
    $('#create_user').click(function() {FirstTime.initialize(INFO.currentUrl)});
    $('body').click(function(e){
        if ($(e.target).hasClass('close_button')) $(e.target).parent().fadeOut();
        if ($(e.target).hasClass('show_help')) $('#welcome').fadeIn();
        if ($(e.target).hasClass('show_create')) FirstTime.initialize(INFO.currentUrl);      
    });
});
