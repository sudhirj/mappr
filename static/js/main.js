google.load("maps", "2");
google.load("jquery", "1.2");
google.load("jqueryui", "1.5");
google.setOnLoadCallback(function(){
    jQuery.delegate = function(rules) {
      return function(e) {
        var target = $(e.target);
        for (var selector in rules)
          if (target.is(selector)) return rules[selector].apply(this, $.makeArray(arguments));
      }
    };
    Map.initialize("map");
    $(document).ready(function() {
        // Pinn creation
        $('#add-point').click(function() {PointMaker.create();});
        $('#points').click($.delegate({
            '.edit': function(e){
                var point = $(e.target).parents('.point');
                var key = $('.key',point).text();
                PointMaker.edit(key);
            },
            '.delete': function(e){
                var point = $(e.target).parents('.point');
                var key = $('.key',point).text();
                PointMaker.delete(key);
            }
        }));
        $('#create-user').click(function() {FirstTime.initialize();});
    });
});
