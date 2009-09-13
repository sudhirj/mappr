var FirstTime = function(){
  var dialog = null;
  var open = false;
  var oldValue = '';
  var readyFlag = false;
  var urlBox = $('input#text-url');
  var errorLabel = $('.error',this.dialog);
  var createButton = $('#create-button');
  return {
    initialize: function(url){
      url = url || '';
      if (this.open) return;
      if (this.dialog == null)  {
        this.dialog = $('#dialog-create-user').show().dialog({
          autoOpen:false,
          draggable:true,
          resizable:false,
          close: function(){FirstTime.cancel();},
          title: "Create a PinnSpot",
          height:230,
          width: 600,
          modal: true,
          overlay: {
            'background':'#000',
            'opacity':0.5
          }
        });
        FirstTime.ready();
        urlBox.keyup(function(e){
          if (e.keyCode == 13) FirstTime.save();
          else{
            var currentValue = urlBox.val();
            if (FirstTime.oldValue == currentValue) return;
            $.get(ROUTES.URL.check(currentValue), null, function(data, status){
              if (data == 'Y') FirstTime.ready();
              else FirstTime.notReady();
              },"text");     
              FirstTime.oldValue = currentValue;                
            } 
          });
          urlBox.keypress(function(e){
            if(e.which == 13 || e.which == 8 || e.which == 0) return true;
            if(48 <= e.which && e.which <= 57) return true;
            if(65 <= e.which && e.which <= 90) return true;
            if(97 <= e.which && e.which <= 122) return true;
            return false;                 
          });
        }
        errorLabel.text('');
        this.dialog.dialog("open");
        urlBox.val(url).focus();
        createButton.click(function(){FirstTime.save()});
        this.open = true;
      },
      cancel: function(){
        this.open = false;
      },
      save: function(){
        if (!this.readyFlag || !this.validate()) return;
        var url = urlBox.val();

        if (!INFO.auth) {window.location = ROUTES.URL.create(url);FirstTime.close(); return;}
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
        var url = urlBox.val();
        if ($.trim(url) == ''){
          errorLabel.text('You need to provide a url for your PinnSpot.');
          return false;
        }
        //TODO: add regex validation to allow only letters and numbers. 
        return true;
      },
      ready: function(){
        urlBox.addClass('green-border').removeClass('red-border');
        createButton.addClass('ok').removeClass('cancel').text('Create!');   
        this.readyFlag = true;     
      },
      notReady: function(){
        urlBox.addClass('red-border').removeClass('green-border');
        createButton.addClass('cancel').removeClass('ok').text('That\'s been taken :(');
        this.readyFlag = false;
      }
    };
  }
  ();