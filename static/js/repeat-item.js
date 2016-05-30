(function($){
    var ij = 0;
	function add_item_option($this, i) {
		$this.find('select.repeatable-items').append('<option value="' + i + '" selected="selected">' + i + '</option>');
	}
	function remove_item_option($this, i) {
		$this.find('select.repeatable-items option[value="' + i + '"]').remove();
	}
    $(document).on('click', '.minus-item', function(){
        var $this = $(this);
        var $repeatable_wrap = $this.parents('.repeatable-wrap');
        var item_id = $this.attr('data-itemId');
        remove_item_option($repeatable_wrap, item_id);
        $repeatable_wrap.find('.repeatable_' + item_id).remove();
    });
    $('.plus-item').click(function() {
        var $this = $(this);
        var $repeatable_wrap = $this.parents('.repeatable-wrap');
        var repeatable_html = $repeatable_wrap.find('.repeatable')[0].outerHTML;
        var $repeat = $repeatable_wrap.find('.repeat');
        var item_id = --ij;
        $repeat.before(repeatable_html);
        var $new_item = $repeat.prev();
        $new_item.addClass('repeatable_' + item_id);
        $new_item.find('select, input, textarea').each(function() {
            var $this = $(this);
            var name = $this.attr('name');
            $this.attr('name', name + '_' + item_id);
        });
        $new_item.find('.minus-item').attr('data-itemId', item_id);
        $new_item.show();
        add_item_option($repeatable_wrap, item_id);
    });
})(jQuery);


