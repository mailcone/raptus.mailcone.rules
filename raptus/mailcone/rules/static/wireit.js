wireit = {
    init: function(){
        wireit.toolbox();
        wireit.toolbox_button();
    },


    toolbox: function(){
        var dialog = $('#wireit-toolbox');
        ui_elements._init_dialog(dialog);
        dialog.dialog('option', 'modal', false );
        dialog.dialog('option', 'width', 200 );
        dialog.dialog( 'option', 'position', [200,200] );
        dialog.dialog( 'option', 'closeOnEscape', false );
        dialog.parent().find('.ui-dialog-titlebar-close').remove();
        var buttons = {};
        buttons[$('#wireit-save').remove().val()] = wireit.submit_workspace;
        dialog.dialog('option', 'buttons', buttons);
        dialog.dialog('close').dialog('open');// fix modal option
        ui_elements.init(dialog);
    },
    
    
    toolbox_button: function(){
        $('.wireit-ruleitem button').each(function(){
            $(this).mousedown(function(event){
                box = wireit.build_rulebox($(this).data('data'));
                box.css('left', event.pageX);
                box.css('top', event.pageY);
                box.draggable({stop: function(event, ui){
                    $(this).draggable('destroy');
                    $(this).removeClass('skeleton');
                }});
                box.trigger(event);console.log(event);
            });
        });
    },
    
    
    submit_workspace: function(){
        
    },
    
    
    build_rulebox: function(data){
        var template = $('#wireit-rulebox-template').html();
        $('#wireit-workspace').append(template);
        return $('#wireit-workspace>.wireit-rulebox');
    },
    
}

jQuery(document).ready(wireit.init);
