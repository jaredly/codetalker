jQuery.fn.debug = function() {
  return this.each(function(){
    alert(this);
  });
};
jQuery.log = function(message) {
  if(window.console) {
     console.debug(message);
  } else {
     alert(message);
  }
};
