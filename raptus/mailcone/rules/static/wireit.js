wireit = {
    init: function(){
        wireit.yui_patch();
        wireit._form_controls_mapping();
        wireit.toolbox();
        wireit.toolbox_button();
        wireit.load_workspace();
    },


    toolbox: function(){
        var dialog = $('#wireit-toolbox');
        ui_elements._init_dialog(dialog);
        
        dialog.dialog('option', 'modal', false);
        dialog.dialog('option', 'width', 200 );
        dialog.dialog( 'option', 'position', [200,200]);
        dialog.dialog( 'option', 'closeOnEscape', false );
        dialog.dialog( 'option', 'zIndex', 900 );
        dialog.dialog( 'option', 'resizable', false );
        dialog.dialog( 'option', 'draggable', false );
        dialog.parent().find('.ui-dialog-titlebar-close').remove();
        
        
        var buttons = {};
        buttons[$('#wireit-save').remove().val()] = wireit.submit_workspace;
        dialog.dialog('option', 'buttons', buttons);
        
        dialog.dialog('close').dialog('open');// fix modal option
        
        ui_elements.init(dialog);
        
        //we should use something else than a dialogbox :S
        dialog.parent().css({
           top: 122,
           left: 380,
           //height: 411,
           borderTopRightRadius: 0,
           borderBottomRightRadius: 0,
        });
        
        $(window).bind('resize', function(){
           var h = $('#wireit-workspace').height();
           h -= dialog.parent().find('.ui-dialog-buttonpane').outerHeight(true);
           h -= dialog.parent().find('.ui-dialog-titlebar').outerHeight(true);
           
           dialog.css({
              height: h
           });
           
        }).trigger('resize');
        
        /* the css is used only for this dialogbox... */
        dialog.parent().find('.ui-dialog-titlebar').css({
           borderTopRightRadius: 0,
        });
        
        dialog.find('.ui-accordion-header, .ui-accordion-content').css({
           borderRadius: 0,
           borderLeft: 'none',
           borderRight: 'none',
        });
        
        dialog.css({padding: 0});
    },
    
    
    toolbox_button: function(){
        var board = $('#wireit-workspace');
        board.droppable({ accept: '.wireit-rulebox' });
        
        $('.wireit-ruleitem button').each(function(){
            $(this).css({background: '#FFF !important'});
            $(this).click(function(){
                $('.wireit-rulebox.skeleton.ui-draggable').remove();
            });
            $(this).mousedown(function(event){
                box = wireit.build_rulebox();
                wireit.init_rulebox(box, $(event.originalEvent.target).parents('a').find('button').data('metadata'));
                var left = event.pageX - box.parent().offset().left+board.scrollLeft();
                var top = event.pageY -box.parent().offset().top+board.scrollTop();
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
                test = box;
                eve = event;
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

        if (!ui_elements.datatable_controls_mapping)
            ui_elements.datatable_controls_mapping = {};
        ui_elements.datatable_controls_mapping['ui-datatable-console']= wireit._datatable_control_console;
    },
    
    
    submit_workspace: function(){
        $('#wireit-workspace').scrollTop(0).scrollLeft(0);
        
        var di = {ruleitems:[],
                  relations:[]};
        $('.wireit-rulebox:not(#wireit-rulebox-template)').each(function(){
            wireit.data_crawler($(this));
            di.ruleitems.push($(this).data('metadata'));
            $.merge(di.relations, wireit.relation_crawler($(this)));
        });
        var form = $('body').append('<form method="post">'+
                     '<input type="hidden" name="metadata" value=""/>'+
                     '</form>').find('form:last');
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
      $.each(data.relations, function(index, rel){
          wireit.yui_add_wire(rel);
      });
    },
    
    
    data_crawler: function(box){
        var data = box.data('metadata');
        data['id'] = box.attr('id');
        data['position'] = box.position();
    },
    
    
    relation_crawler: function(box){
        list = [];
        $.each(box.data('terminals'), function(index, terminal){
            $.each(terminal.wires, function(index, wire){
                var t1 = $(wire.terminal1.el);
                var t2 = $(wire.terminal2.el);
                if (t2.parents('.wireit-rulebox').attr('id') == box.attr('id'))
                    return;
                list.push({ terminal1:{object_id:t1.parents('.wireit-rulebox').attr('id'),
                                       terminal_id:wire.terminal1.id },
                            terminal2:{object_id:t2.parents('.wireit-rulebox').attr('id'),
                                       terminal_id:wire.terminal2.id }});
            });
        });
        return list;
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

    _datatable_control_console: function(){
      $(this).click(function(){
          var dialog = $('#ui-modal-content');
          var mail = $(this).attr('href').match(/\?mail=(.*)$/)[1];
          var box = $(wireit.lastbuttonevent.target).parents('.wireit-rulebox');
          var di = {ruleitem_to_verify: box.attr('id'),
                    mail_to_verify: mail,
                    ruleitems:[],
                    relations:[]};
          $('.wireit-rulebox:not(#wireit-rulebox-template)').each(function(){
              wireit.data_crawler($(this));
              di.ruleitems.push($.extend({},$(this).data('metadata')));
              $.merge(di.relations, wireit.relation_crawler($(this)));
          });
          $.each(di.ruleitems, function(index, item){
              if (item.id == box.attr('id')){
                  item['properties'] = ui_elements._data_collector(dialog);
              }
          });
          var data = JSON.stringify(di);
          data = {metadata:data};
          $.post($(this).attr('href'), data,function(data){
              $('#ui-console').append('<br/>'+data);
          });
          return false;
      });
    },


    _form_controls_save: function(){
        var dialog = $('#ui-modal-content');
        var box = $(wireit.lastbuttonevent.target).parents('.wireit-rulebox');
        var data = box.data('metadata');
        var di = ui_elements._data_collector(dialog);
        data['properties'] = di;
        wireit.update_rulebox(box);
        dialog.dialog('close');
    },


    build_rulebox: function(uid){
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
        // must be a copy of the dict. $.extend do this! 
        box.data('metadata', $.extend({},data));
        ui_elements.init(box);
        wireit.yui_boxinit(box);
    },
    
    
    update_rulebox: function(box){
        var data = box.data('metadata');
        if (data.properties['properties.title'])
            box.find('.boxtitle').html(data.properties['properties.title']+' <em>('+data.title+')</em>');
        else
            box.find('.boxtitle').html('<em>'+data.title+'</em>');
        box.find('.boxdescription').html(data.properties['properties.description']);
    },
    
    
    rulebox_fill_data: function(box, dialog){
        var data = box.data('metadata');
        var prop = data.properties?data.properties:{};
        dialog.find('input, select, textarea, code').each(function(){
            var name = $(this).attr('name');
            if (name in prop){
                if ($(this).is(':checkbox')){
                    $(this).attr('checked', prop[name]);
                    return;
                }
                // need a special hook for code widget (codemirror)
                if($(this).is('code'))
                    $(this).text(prop[name]);
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
            var settings = {offsetPosition: [x,-22], nMaxWires:Infinity};
            var terminal = new WireIt.util.TerminalInput(block, $.extend(settings, term.data));
            terminal.id = term.id; // patch id on object
            terminals.push(terminal);
        });
        $.each(data.output, function(index, term){
            var y = box.height() - 7; // terminal width correction
            var li = $(box.find('.boxbottom li')[index]);
            var x = li.position().left + li.width()/2 - 3; // terminal width correction
            var settings = {offsetPosition: [x,y]};
            var terminal = new WireIt.util.TerminalOutput(block, $.extend(settings, term.data));
            terminal.id = term.id; // patch id on object
            terminals.push(terminal);
        });
        box.data('terminals', terminals);
        
        new WireIt.util.DD(terminals, block);
    },
    
    
    yui_add_wire: function(rel){
        var t1, t2;
        $.each($('#'+rel.terminal1.object_id).data('terminals'), function(index, term){
            if (rel.terminal1.terminal_id == term.id)
                t1 = term;
        });
        $.each($('#'+rel.terminal2.object_id).data('terminals'), function(index, term){
            if (rel.terminal2.terminal_id == term.id)
                t2 = term;
        });
        var parent = YAHOO.util.Dom.get('wireit-workspace');
        wire = new WireIt.Wire(t1, t2, parent, {});
        wire.redraw();
    },
    
    
    yui_patch: function(){
        // monkey-patch >:-)
        var board = $('#wireit-workspace');
        
        
        var marginLeft = 15;
        var marginTop = 15;
        
        var old_function = WireIt.Terminal.prototype.getXY;
        var new_function = function(){
            box = $(this.el).parent().position();
            ter = $(this.el).position();
            
            return [box.left + ter.left + 15 + board.scrollLeft(), box.top + ter.top + 15 + board.scrollTop()];
        }
        WireIt.Terminal.prototype.getXY = new_function;
        
        var old_function = WireIt.TerminalProxy.prototype.startDrag;
        var new_function = function(){
            re = old_function.call(this);
            this.fakeTerminal.getXY = function() {
                var org = board.offset();
                return [this.pos[0]-org.left/* + 15*/ + board.scrollLeft(), this.pos[1]-org.top/* + 15*/ + board.scrollTop()];
            }
            return re;
        }
        WireIt.TerminalProxy.prototype.startDrag = new_function;
    },
    
}

jQuery(document).ready(wireit.init);


