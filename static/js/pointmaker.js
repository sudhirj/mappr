
var PointMaker = function(){
    var CREATE = 'CREATE';
    var EDIT = 'EDIT';
    var marker = null;
    var dialog = null;
    var open = false;
    var dialogOpts = {
        autoOpen:false,
        draggable:true,
        resizable:false,
        close: function(){PointMaker.cancel();},
        show:'drop',
        hide:'drop'
    };
    var saveMode = 'C';
    return {
        initialize: function(opts){
            var defaults = {mode:CREATE};
            var opts = $.extend(defaults, opts) || {};
            if (this.open) return;
            if (this.dialog == null)
            {
                var title = (opts.mode=='C')? "Push a new Pinn" : "Change this Pinn";
                $.extend(dialogOpts, {title:title});
                this.dialog = $('#dialog-add-point').show().dialog(dialogOpts);
                $('.ok.button',this.dialog).click(function() {PointMaker.save()});
                $('.cancel.button',this.dialog).click(function(){PointMaker.close();})
            }
            $('.error',this.dialog).text('');
            $('input#text-title',this.dialog).val('');
            this.dialog.dialog("open");
            var center = Map.map.getCenter();
            this.marker = Map.addMarker({point:center,draggable:true});
            this.open = true;
        },
        cancel: function(){
            Map.map.removeOverlay(PointMaker.marker);
            PointMaker.marker = null;
            this.open = false;
        },
        save: function(){
            var title = $('input#text-title',PointMaker.dialog).val();
            if (!this.validate()) return;
            $.ajax({
                url: '/_points/',
                type: 'POST',
                data:{
                    title: title,
                    lat: PointMaker.marker.getLatLng().lat(),
                    lon: PointMaker.marker.getLatLng().lng()
                },
                dataType: 'text',
                error: function(response,status,error){
                    $('.error',this.dialog).text(response.responseText);
                },
                success: function(data){
                    PointMaker.close();
                    $('#points').load('/_points/'+INFO.currentUrl);
                    $(PointMaker).trigger('pointCreated');
                    
                }
            });
        },
        validate: function(){
            var title = $('input#text-title',this.dialog).val();
            if ($.trim(title) == '')
            {
                $('.error',this.dialog).text('You need to provide a title for this Pinn.');
                return false;
            }
            return true;
        },
        close: function(){
            PointMaker.dialog.dialog('close');
        }
    };
}
();
