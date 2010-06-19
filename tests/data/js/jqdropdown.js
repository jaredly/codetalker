// jqdropdown jquery plugin, used by widthpicker.js
// uses factory function 'jQueryPlugin' defined in inputslider.js
/*jslint indent:2 */
(function($){

  jQueryPlugin('jqdropdown', {
      value:'',
      options:[],
      onShow:function(){},
      onHide:function(){},
      onChange:function(ddown, value, real){},
    }, {
      // helpers...
      options:'setOptions',
      value:'setValue',
      clear:null, // maps to this.clear
      show:null,
      hide:null,
    },
    function init(settings) {
      var that = this, optionChange;
      that.input = $('<input value="'+settings.value+'"/>').appendTo(that.node);

      that.setValue = function(value) {
        if (typeof(value) === 'undefined')
          return settings.value;
        that.input.val(value);
        settings.value = value;
        settings.real = null;
      };
      that.change = function(value) {
        var val = settings.onChange.call(that.node, that, value);
        if (typeof(val) !== 'undefined')
          value = val;
        settings.value = value;
        that.input.val(value);
      };
      that.setOptions = function(options) {
        that.settings.options = options;
        that.clear();
        that.makeOptions();
      };
      that.clear = function() {
        $('div.option', that.node).remove();
      };
      that.show = function() {
        settings.value = that.input.val();
        if (settings.onShow.call(that.node, that, settings.value) === false)
          return;
        $('div.option:contains('+that.input.val()+')').addClass('hidden');
        $('div.option', that.node).show();
      };
      that.hide = function() {
        if (settings.onHide.call(that.node, that, settings.value) === false)
          return;
        $('div.option', that.node).hide().removeClass('hidden');
      };
      that.showHide = function() {
        if ($('div.option', that.node).css('display') === 'block')
          that.hide();
        else
          that.show();
      };
      optionChange = function() {
        that.change(this.innerHTML);
      };
      that.makeOptions = function() {
        var val, cls, i;
        for (i=0;i<settings.options.length;i+=1){
          val = settings.options[i];
          cls = '';
          if (val instanceof Array) {
            cls = val[1] || '';
            val = val[0];
          }
          $('<div class="option '+cls+'">'+val+'</div>').appendTo(that.node)
            .click(optionChange);
        }
        that.hide();
      };
      that.makeOptions();
      that.node.click(that.showHide);
      that.input.blur(function(){
          that.change(this.value);
        });
      that.input.keydown(that.hide);
      that.hide();
    }
  );
}(jQuery));
