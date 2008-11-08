
var Message = function(){
    return {
        show: function(o){
            var defaults = {
                msg: ""
            }
            var o = $.extend(defaults, o || {});
            body = $('body');
            msgbox = $('#info-message');
            var bh = body.height(); var bw = body.width();
            msgbox.html(o.msg).show();
            var bottom = (1/8*bh)+'px'; var left = ((bw-msgbox.outerWidth())/2);
            msgbox.css({bottom:bottom , left: left});
        },
        hide: function(){
            $('#info-message').hide();
        }
    };
}
();
