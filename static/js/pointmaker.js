var PointMaker = function(){
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
    var data = null;
    return {
        create: function(){
            if (this.isOpen) PointMaker.close();
            var center = Map.map.getCenter();
            this.data = {
                dialogTitle: "Push a new Pinn",
                title: "",
                point: center
            };
            this.initialize();
            $('#text-title').val('');
        },
        edit: function(key){
            if (this.isOpen) PointMaker.close();
            var point = $('#points .point:has(.key:contains('+key+'))');
            var lat = $('.lat',point).text();
            var lon = $('.lon',point).text();
            var title = $('.title',point).text();
            var latlon = new google.maps.LatLng(lat,lon);

            this.data = {
                dialogTitle: "Change this Pinn",
                key: key,
                point: latlon
            };          
            this.initialize();          
            $('#text-title').val(title);
        },
        del: function(key){
            var answer = confirm('Are you sure you want to delete this Pinn?');
            if (!answer) return;
            if (this.isOpen) this.close();
            $.ajax({
                url: '/_points/delete/',
                type: 'POST',
                data: {key: key},
                success: PointMaker.update
            });
        },
        initialize: function(){
            if (this.isOpen) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-add-point').show().dialog(dialogOpts);
                $('.ok.button',this.dialog).click(function() {PointMaker.save()});
                $('.cancel.button',this.dialog).click(function() {PointMaker.close()})
            }
            $('.error',this.dialog).text('');
            $('span.ui-dialog-title',this.dialog.parent()).text(this.data.dialogTitle);
            this.dialog.dialog("open");

            this.marker = Map.addMarker({point:this.data.point,draggable:true});
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
            var pointData = {
                title: title,
                lat: PointMaker.marker.getLatLng().lat(),
                lon: PointMaker.marker.getLatLng().lng()
            };
            if (this.data.key) $.extend(pointData,{key:this.data.key});            
            $.ajax({
                url: '/_points/',
                type: 'POST',
                data: pointData,
                dataType: 'text',
                error: function(response,status,error){
                    $('.error',this.dialog).text(response.responseText);
                },
                success: function(data){
                    PointMaker.close();
                    PointMaker.update();
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
            if (this.isOpen) this.dialog.dialog('close');
        },
        update: function(){
            $('#points').load('/_points/'+INFO.currentUrl);
        }
    };
}
();