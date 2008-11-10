var PointMaker = function(){
    var Modes = {
      CREATE: 'CREATE',
      EDIT: 'EDIT'  
    };
    var marker = null;
    var dialog = null;
    var isOpen = false;
    var dialogOpts = {
        autoOpen:false,
        draggable:true,
        resizable:false,
        close: function(){PointMaker.cancel();},
        show:'drop',
        hide:'drop',
        position: [100,50]
    };
    var mode = Modes.CREATE;
    var data = null;
    return {
        create: function(){
            this.data = {
                dialogTitle: "Push a new Pinn"
            };
        },
        edit: function(){
            this.data = {
                dialogTitle: ""
            };
        },
        initialize: function(opts){
            var defaults = {mode:Modes.CREATE};
            var opts = $.extend(defaults, opts || {});
            if (this.isOpen) return;
            if (this.dialog == null)
            {
                $.extend(dialogOpts, {title:data.dialogTitle});
                this.dialog = $('#dialog-add-point').show().dialog(dialogOpts);
                $('.ok.button',this.dialog).click(function() {PointMaker.save()});
                $('.cancel.button',this.dialog).click(function() {PointMaker.close()})
            }
            $('.error',this.dialog).text('');
            $('input#text-title',this.dialog).val('');
            this.dialog.dialog("open");
            var center = Map.map.getCenter();
            this.marker = Map.addMarker({point:center,draggable:true});
            this.isOpen = true;
        },
        cancel: function(){
            Map.map.removeOverlay(PointMaker.marker);
            PointMaker.marker = null;
            this.isOpen = false;
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