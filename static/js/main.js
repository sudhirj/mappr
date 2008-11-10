google.load("maps", "2");
google.load("jquery", "1.2");
google.load("jqueryui", "1.5");
google.setOnLoadCallback(function(){
    Map.initialize("map");
    $(document).ready(function() {
        $('#add-point').click(function() {PointMaker.initialize();});
        $('#create-user').click(function() {FirstTime.initialize();});
    });
});
