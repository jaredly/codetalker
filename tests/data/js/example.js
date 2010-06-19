 (function($) {
 
   $.fn.myPlugin = function(settings) {
     var config = {'foo': 'bar'};
 
     if (settings) $.extend(config, settings);
 
     this.each(function() {
       // element-specific code here
     });
 
     return this;
 
   };
 
 })(jQuery);
