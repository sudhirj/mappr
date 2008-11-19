google.load("maps", "2");
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
    });
    Map.initialize("map");    
    $(document).ready(function() {
        PointList.initialize();        
        $('#create-user').click(function() {FirstTime.initialize();});    
               
    });
});