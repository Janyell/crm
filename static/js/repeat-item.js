function update_attr_name ($this, i) {
    var name = $this.attr('name');
    var new_name;
    var brackets_index = name.indexOf('[]');
    if (brackets_index == -1) {
        new_name = name + '_' + i;
    }
    else {
        new_name = name.substr(0, brackets_index) + '_' + i + '[]';
    }
    $this.attr('name', new_name);
}
function update_item_id ($new_item, item_id) {
    $new_item.addClass('repeatable_' + item_id);
    var $new_control_group = $new_item.children('.control-group');
    $new_control_group.find('select, input, textarea').each(function () {
        update_attr_name($(this), item_id)
    });
    $new_control_group.find('.minus-item').attr('data-itemId', item_id);
}

function add_item_option($this, i) {
    $this.children('select.repeatable-items').append('<option value="' + i + '" selected="selected">' + i + '</option>');
}
function remove_item_option($this, i) {
    $this.children('select.repeatable-items option[value="' + i + '"]').remove();
}

function handle_click($this, item_id, click_children) {
    var $repeatable_wrap = $this.closest('.repeatable-wrap');
    var repeatable_html = $repeatable_wrap.children('.repeatable')[0].outerHTML;
    var $repeat = $repeatable_wrap.children('.repeat');
    $repeat.before(repeatable_html);
    var $new_item = $repeat.prev();
    update_item_id($new_item, item_id);
    var $new_children_repeatable_wrap = $new_item.children('.repeatable-wrap');
    if ($new_children_repeatable_wrap.size()) {
        update_attr_name($new_children_repeatable_wrap.children('select.repeatable-items'), item_id);
        if (click_children) {
            $new_children_repeatable_wrap.children('.repeat').find('.plus-item').click();
        }
    }
    $new_item.show();
    add_item_option($repeatable_wrap, item_id);
    return $new_item;
}
(function($){
    var ij = 0;
    $(document).on('click', '.minus-item', function(){
        var $this = $(this);
        var $repeatable_wrap = $this.closest('.repeatable-wrap');
        var item_id = $this.attr('data-itemId');
        remove_item_option($repeatable_wrap, item_id);
        $repeatable_wrap.find('.repeatable_' + item_id).remove();
    });
    $(document).on('click', '.plus-item', function() {
        handle_click($(this), --ij, true);
    });
})(jQuery);

