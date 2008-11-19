var FirstTime = function(){
    var dialog = null;
    var open = false;
    var currentValue;
    return {
        initialize: function(url){
            if (!url) url = '';
            if (this.open) return;
            if (this.dialog == null)
            {
                this.dialog = $('#dialog-create-user').show().dialog({
                    autoOpen:false,
                    draggable:true,
                    resizable:false,
                    close: function(){FirstTime.cancel();},
                    title: "Create a PinnSpot"
                });
                FirstTime.ready();
                $('#text-url').keyup(function(e){
                    if (e.keyCode == 13) FirstTime.save();
                    else{
                        currentValue = $('#text-url').val();
                        $.get('/_check/url/'+currentValue,null,function(data,status){
                            if (data == 'Y') FirstTime.ready();
                            else FirstTime.notReady();
                        },"text");                     
                    } 
                });
                $('#text-url').keypress(function(e){
                    if(e.which == 13 || e.which == 8 || e.which == 0) return true;
                    if(48 <= e.which && e.which <= 57) return true;
                    if(65 <= e.which && e.which <= 90) return true;
                    if(97 <= e.which && e.which <= 122) return true;
                    return false;                 
                });
            }
            $('.error',this.dialog).text('');
            $('input#text-url',this.dialog).val(url);
            $('#dynamic-url').text(url);
            this.dialog.dialog("open");
            $('input#text-url',this.dialog)[0].focus();
            $('#create-button').click(function(){FirstTime.save()});
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
                    FirstTime.notReady();
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
        },
        ready: function(){
            $('#text-url').addClass('green-border').removeClass('red-border');
            $('#create-button').addClass('ok').removeClass('cancel').text('Create!');   
            $('#dynamic-url').text($('#text-url').val());         
        },
        notReady: function(){
            $('#text-url').addClass('red-border').removeClass('green-border');
            $('#create-button').addClass('cancel').removeClass('ok').text('That\'s been taken :(');
        }
    };
}
();