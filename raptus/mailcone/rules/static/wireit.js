wireit = {
    init: function(){
        wireit._form_controls_mapping();
        wireit.toolbox();
        wireit.toolbox_button();
        wireit.load_workspace();
    },


    toolbox: function(){
        var dialog = $('#wireit-toolbox');
        ui_elements._init_dialog(dialog);
        dialog.dialog('option', 'modal', false );
        dialog.dialog('option', 'width', 200 );
        dialog.dialog( 'option', 'position', [200,200] );
        dialog.dialog( 'option', 'closeOnEscape', false );
        dialog.dialog( 'option', 'zIndex', 900 );
        dialog.parent().find('.ui-dialog-titlebar-close').remove();
        var buttons = {};
        buttons[$('#wireit-save').remove().val()] = wireit.submit_workspace;
        dialog.dialog('option', 'buttons', buttons);
        dialog.dialog('close').dialog('open');// fix modal option
        ui_elements.init(dialog);
    },
    
    
    toolbox_button: function(){
        $('#wireit-workspace').droppable({ accept: '.wireit-rulebox' });
        $('.wireit-ruleitem button').each(function(){
            $(this).mousedown(function(event){
                box = wireit.build_rulebox();
                wireit.init_rulebox(box, $(event.originalEvent.target).parents('a').find('button').data('metadata'));
                var left = event.pageX - box.parent().offset().left;
                var top = event.pageY -box.parent().offset().top;
                box.css('left',left);
                box.css('top', top);
                box.draggable({ revert: function(event){
                                    if (event)
                                        return;
                                $(this).animate({left: left,
                                                 top:  top},
                                                 200,
                                                 'swing',
                                                 function(){$(this).remove()});
                              },
                                stop: function(){
                                $(this).draggable('destroy');
                                $(this).removeClass('skeleton');
                }});
                box.trigger(event);
            });
        });
    },
    
    
    _form_controls_mapping: function(){
        if (!ui_elements.form_controls_mapping)
            ui_elements.form_controls_mapping = {};
        ui_elements.form_controls_mapping['form.actions.wireit_delete'] = wireit._form_controls_delete;
        ui_elements.form_controls_mapping['properties.actions.wireit_save'] = wireit._form_controls_save;
        ui_elements.form_controls_mapping['properties.actions.cancel']= ui_elements._form_controls_cancel;
    },
    
    
    submit_workspace: function(){
        var di = {ruleitems:[]};
        $('.wireit-rulebox:not(#wireit-rulebox-template)').each(function(){
            wireit.data_crapper($(this));
            di.ruleitems.push($(this).data('metadata'));
        });
        var form = $('body').append('<form method="post">'+
                     '<input type="hidden" name="metadata" value=""/>'+
                     '</form>').find('form:last');console.log(di);
        form.find('input').val(JSON.stringify(di));
        form.submit();
    },
    
    
    load_workspace:function(){
      var data = $('#wireit-workspace').data('json_data');
      $.each(data.ruleitems, function(index, item){
          var box = wireit.build_rulebox(item.id);
          wireit.init_rulebox(box, item);
          wireit.update_rulebox(box);
          box.removeClass('skeleton');
      });
    },
    
    
    data_crapper: function(box){console.log(box);
        var data = box.data('metadata');
        data['id'] = box.attr('id');
        data['position'] = box.position();
        
        box.data('metadata', data);console.log(box.data('metadata'));console.log(data);
    },
    
    
    _form_controls_delete: function(){
        var dialog = $('#ui-modal-content');
        var box = $(wireit.lastbuttonevent.target).parents('.wireit-rulebox');
        $.each(box.data('terminals'),function(index,term){
            term.removeAllWires();
        });
        
        box.remove();
        dialog.dialog('close');
    },


    _form_controls_save: function(){
        var dialog = $('#ui-modal-content');
        var box = $(wireit.lastbuttonevent.target).parents('.wireit-rulebox');
        var data = box.data('metadata');
        var di = {};
        dialog.find('input, textarea, select').val(function(index, value){
            if ($(this).is(':checkbox')){
                //special case for ckeckboxes, maybe we need some more..
                di[$(this).attr('name')] = $(this).is(':checked');
                return;
            }
            di[$(this).attr('name')] = value;
        });
        data['properties'] = di;
        box.data('metadata', data);
        wireit.update_rulebox(box);
        dialog.dialog('close');
    },


    build_rulebox: function(uid){console.log(uid);
        var clone = $('#wireit-rulebox-template').clone();
        if (!uid)
            var uid = wireit.uid();
        clone.attr('id', uid);
        $('#wireit-workspace').append(clone);
        return clone;
    },
    
    
    init_rulebox: function(box, data){
        if (data.position)
            box.css('top', data.position.top).css('left', data.position.left);
            
        box.find('.boxtitle').html(data.title);
        $.each(data.input, function(index, term){
            box.find('.boxtop').append('<li>'+term.title+'</li>');
        });
        $.each(data.output, function(index, term){
            box.find('.boxbottom').append('<li>'+term.title+'</li>');
        });
        $.each(data.buttons, function(index, button){
            $(this).data('postdata', data.identifer);
            box.find('.wireit-rulebox-control').append('<button class="'+button.cssclass+'"'+
                                                       'data-ui-icon="'+button.icon+'"'+
                                                       'href="'+button.ajax+'">'+button.title+'</button>');
            box.find('.wireit-rulebox-control>button:last').click(function(event){
                wireit.lastbuttonevent = event;
                var callback = function(dialog){
                    wireit.rulebox_fill_data(box, dialog);
                }
                ui_elements._ajax_modal(button.ajax, $(this), {identifer:JSON.stringify(data.identifer)}, callback);
            });
        });
        box.data('metadata', data);
        ui_elements.init(box);
        wireit.yui_boxinit(box);
    },
    
    
    update_rulebox: function(box){
        var data = box.data('metadata');
        box.find('.boxtitle').html(data.properties['properties.title']+' <em>('+data.title+')</em>');
        box.find('.boxdescription').html(data.properties['properties.description']);
    },
    
    
    rulebox_fill_data: function(box, dialog){
        var data = box.data('metadata');
        var prop = data.properties?data.properties:{};
        dialog.find('input, select, textarea').each(function(){
            var name = $(this).attr('name');
            if (name in prop){
                if ($(this).is(':checkbox')){
                    $(this).attr('checked', prop[name]);
                    return;
                }
                $(this).val(prop[name]);
            }
        });
    },
    
    
     uid: function() {
        // http://jsfiddle.net/7sXL6/
        var result, i, j;
        result = '';
        for(j=0; j<32; j++) {
            if( j == 8 || j == 12|| j == 16|| j == 20)
                result = result + '-';
            i = Math.floor(Math.random()*16).toString(16).toUpperCase();
            result = result + i;
        }
        return result;
    },
    
    
    yui_boxinit: function(box){
        var boxid = box.attr('id');
        var data = box.data('metadata');
        var block = YAHOO.util.Dom.get(boxid);
        var terminals = [];
        $.each(data.input, function(index, term){
            var li = $(box.find('.boxtop li')[index]);
            var x = li.position().left + li.width()/2 - 3; // terminal width correction
            terminals.push(new WireIt.util.TerminalInput(block, {direction: [-1,-1], offsetPosition: [x,-22]}));
        });
        $.each(data.output, function(index, term){
            var y = box.height() - 7; // terminal width correction
            var li = $(box.find('.boxbottom li')[index]);
            var x = li.position().left + li.width()/2 - 3; // terminal width correction
            terminals.push(new WireIt.util.TerminalOutput(block, {direction: [1,1], offsetPosition: [x,y]}));
        });
        box.data('terminals', terminals);
        
        new WireIt.util.DD(terminals, block);
    },
    
}

jQuery(document).ready(wireit.init);

// YUI and WireIt stuff

WireIt.util.MailconeDD = function( terminals, id, layer, sGroup, config) {
    WireIt.util.MailconeDD.superclass.constructor.call(this, terminals, id, sGroup, config);
    this.layer = layer;
    this.initTerminals();
    this.initOptions();
};

YAHOO.lang.extend(WireIt.util.MailconeDD, WireIt.util.DD, {

    initTerminals: function() {
      for(var i = 0 ; i < this._WireItTerminals.length ; i++) {
         this._WireItTerminals[i].container= this;
      }
   },
   
   
   initOptions: function() {
        this.options = {};
   },
});

// monkey-patch
window.onload = function(){
    var old_function = WireIt.Terminal.prototype.getXY;
    var new_function = function(){
        box = $(this.el).parent().position();
        ter = $(this.el).position();
        return [box.left + ter.left + 15,box.top + ter.top + 15];
    }
    WireIt.Terminal.prototype.getXY = new_function;
    
    var old_function = WireIt.TerminalProxy.prototype.startDrag;
    var new_function = function(){
        re = old_function.call(this);
        this.fakeTerminal.getXY = function() { 
            var org = $('#wireit-workspace').offset()
            return [this.pos[0]-org.left + 15, this.pos[1]-org.top + 15];
        }
        return re;
    }
    WireIt.TerminalProxy.prototype.startDrag = new_function;
}



/*



window.onload = function() {
    
    // Create 2 terminals into Block1
    var block1 = YAHOO.util.Dom.get('block1');
    var terminals1 = [new WireIt.Terminal(block1, {direction: [-1,0], offsetPosition: [-14,35]}), 
                            new WireIt.Terminal(block1, {direction: [1,0], offsetPosition: [85,35]})];
    
    // Make the block1 draggable
    new WireIt.util.DD(terminals1,block1); 
    
    // Create 2 terminals into Block2
    var block2 = YAHOO.util.Dom.get('block2');
    var terminals2 = [new WireIt.Terminal(block2, {direction: [-1,0], offsetPosition: [-14,35]}), 
                            new WireIt.Terminal(block2, {direction: [1,0], offsetPosition: [85,35]})];
    
    // Make the block2 draggable
    new WireIt.util.DD(terminals2,block2);
    
    // Create a wire between some terminals
    var w1 = new WireIt.BezierWire(terminals1[0], terminals2[0], document.body);
    w1.redraw();
    
    var w2 = new WireIt.BezierWire(terminals1[1], terminals2[1], document.body);
    w2.redraw();
    
};
*/


