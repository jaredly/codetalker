$('#textBoxId').keydown(function(e) {
      if(e.keyCode == 13) {
          e.preventDefault(); 
              $('#buttonId').trigger('click');
                }
                });


$('#textBoxId').keydown(function(event) {
        var e = event || window.event;
            var keyCode = document.all ? e.keyCode : e.which;

                if (keyCode == 13) {
                        e.preventDefault();
                                $('#buttonId')[0].click();
                                    }
                                    });
