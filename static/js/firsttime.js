
var FirstTime = function(){
    var dialog = null;
    var open = false;
    return {
        initialize: function(){
            if (this.open) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-create-user').show().dialog({
                    autoOpen:false,
                    draggable:true,
                    resizable:false,
                    close: function(){FirstTime.cancel();},
                    title: "Create a PinnSpot",
                    show:'drop',
                    hide:'drop'
                });
                $('.ok.button',this.dialog).click(function() {FirstTime.save()});
                $('.cancel.button',this.dialog).click(function(){FirstTime.close()})
            }
            $('.error',this.dialog).text('');
            $('input#text-url',this.dialog).val('');
            this.dialog.dialog("open");
            this.open = true;
        },
        cancel: function(){
            this.open = false;
        },
        save: function(){
            if (!this.validate()) return;
            var url = $('input#text-url',this.dialog).val();

            $.ajax({
                type: "POST",
                url: '/',
                data: {url:url},
                success: function(data){
                    FirstTime.close();
                    $(FirstTime).trigger('urlCreated');
                    window.location = '/'+$.trim(data);
                },
                dataType: "text",
                error: function(response,status,error){
                    $('.error',this.dialog).text(response.responseText);
                }                
            });
        },
        close: function(){
            this.dialog.dialog('close');
        },
        validate: function(){
            var url = $('input#text-url',this.dialog).val();
            if ($.trim(url) == '')
            {
                $('.error',this.dialog).text('You need to provide a url for your PinnSpot.');
                return false;
            }
            //TODO: add regex validation to allow only letters and numbers. 
            return true;
        }
    };
}
();