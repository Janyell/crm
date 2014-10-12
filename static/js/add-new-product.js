(function($){
	var ij = 0;
	function select_product_select_option(i) {
		$('select.product-select option[value="' + i + '"]').attr('selected', 1);	
	}
	function unselect_product_select_option(i) {
		$('select.product-select option[value="' + i + '"]').removeAttr('selected');	
	}
	function add_product_select_selected_option(i) {
		$('select.product-select').append('<option value="' + i + '" selected="1">New</option>');	
	}
	function remove_product_select_option(i) {
		$('select.product-select option[value="' + i + '"]').remove();	
	}

	$(document).on('click', '.plus', function(){
		var $this = $(this);
		var product_id = $this.attr('data-productId');
		var product_title;
		var number = 0;
		if (product_id != null) {
			if ($( '.select-product_' + product_id ).size() != 0)
				return;
			product_title = $this.parent().prev().text();
			select_product_select_option(product_id);
			number = $('select.product-select option[value="' + product_id + '"]').attr('data-number');
			if (!number)
				number = 0;
		}
		else {
			product_id = --ij;
            console.log('sdsds');
            console.log(product_id);
			product_title = '<input type="text" class="select-product__title" name="select-product__title_' + product_id + '" placeholder="Другое">'
			console.log(product_title);
            add_product_select_selected_option(product_id);
		}
		$('.select-product-table__plus').before('<tr class="select-product_' + product_id + '">' +
			'<td>' + product_title + '</td>' +
			'<td><input type="number" min="0" value="'+ number +'" step="1" class="select-product__number" name="select-product__number_' + product_id + '" />' +
			'<td><span class="btn btn-danger minus pull-right" data-productId="' + product_id + '">-</span></td>' +
		'</tr>'
		);

	});
	$(document).on('click', '.minus', function(){
		var product_id = $(this).attr('data-productId');
		if (product_id >= 0) {
			unselect_product_select_option(product_id);
		}
		else {
			remove_product_select_option(product_id);
		}
		$( '.select-product_' + product_id).remove();
	});
})(jQuery);