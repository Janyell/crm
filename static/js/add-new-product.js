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
        var $price;
		var product_id = $this.attr('data-productId');
		var product_title;
        var product_price = 0;
		var number = 1;
		if (product_id != null) {
			if ($( '.select-product_' + product_id ).size() != 0)
				return;
            $price = $this.parent().prev();
            product_price = $price.find('.hidden').text();
            if (!product_price) {
                product_price = 0;
            }
			product_title = $price.prev().text();
			select_product_select_option(product_id);
			number = $('select.product-select option[value="' + product_id + '"]').attr('data-number');
            if (!number) {
                number = 1;
            }
		}
		else {
			product_id = --ij;
			product_title = '<input type="text" class="select-product__title" name="select-product__title_' + product_id + '" placeholder="Другое">';
            add_product_select_selected_option(product_id);
		}
		$('.select-product-table__plus').before('<tr class="select-product select-product_' + product_id + '">' +
			'<td>' + product_title + '</td>' +
            '<td><input type="number" min="0" value="'+ product_price +'" step="1" class="select-product__price" name="select-product__price_' + product_id + '" /></td>' +
			'<td><input type="number" min="0" value="'+ number +'" step="1" class="select-product__number" name="select-product__number_' + product_id + '" /></td>' +
			'<td><span class="btn btn-danger minus pull-right" data-productId="' + product_id + '">-</span></td>' +
		'</tr>'
		);
        countSum();
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
        countSum();
	});
    function countSum() {
        var $products = $('.select-product-table tr.select-product');
        var sum = 0;
        $products.each(function () {
            var $this = $(this);
            var price = $this.find('.select-product__price').val();
            var number = $this.find('.select-product__number').val();
            sum += price * number;
        });
        $('#inputBill').val(sum);
    }
    $(document).on('change', '.select-product__price',function() {
       countSum();
    });
    $(document).on('change', '.select-product__number',function() {
       countSum();
    });
	function addProductToSelectTable(id, title, price, number) {
		$('.select-product-table__plus').before('<tr class="select-product select-product_' + id + '">' +
			'<td>' + title + '</td>' +
            '<td><input type="number" min="0" value="'+ price +'" step="1" class="select-product__price" name="select-product__price_' + id + '" /></td>' +
			'<td><input type="number" min="0" value="'+ number +'" step="1" class="select-product__number" name="select-product__number_' + id + '" /></td>' +
			'<td><span class="btn btn-danger minus pull-right" data-productId="' + id + '">-</span></td>' +
		'</tr>'
		);
        countSum();
	}
	$(document).on('click', 'select.product-select option', function() {
		var $this = $(this);
		addProductToSelectTable($this.attr('value'), $this.text(), $this.attr('data-price'), $this.attr('data-number'));
	});
})(jQuery);