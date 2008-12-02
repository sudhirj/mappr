var PointRegister = function(){
    var list = new Array();
    return {
        initialize: function(){
          
            
        },
        update: function(){
          $.ajax({
            url: "mydomain.com/url",
            type: "POST",
            data: $.param( $("Element or Expression") ),
          
  complete: function() {
              //called when complete
  },
          
  success: function() {
              //called when successful
 },
          
  error: function() {
              //called when there is an error
  },
          });
          
        }
    };
}
();