/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('marketplace_seller_wise_checkout.mp_seller_checkout', function (require) {

    var core = require('web.core');
    var ajax = require('web.ajax');

    $(document).ready(function() {

        $('.oe_website_sale').each(function() {
            var oe_website_sale = this;

            var clickwatch = (function(){
                  var timer = 0;
                  return function(callback, ms){
                    clearTimeout(timer);
                    timer = setTimeout(callback, ms);
                  };
            })();

            $(oe_website_sale).off("change", ".oe_cart input.js_quantity[data-product-id]")
            $(oe_website_sale).on("change", ".oe_cart input.js_quantity[data-product-id]", function () {

                var $input = $(this);
                  if ($input.data('update_change')) {
                      return;
                  }
                var value = parseInt($input.val() || 0, 10);
                var $dom = $(this).closest('tr');
                //var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
                var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
                var line_id = parseInt($input.data('line-id'),10);
                var product_ids = [parseInt($input.data('product-id'),10)];
                clickwatch(function(){
                  $dom_optional.each(function(){
                      $(this).find('.js_quantity').text(value);
                      product_ids.push($(this).find('span[data-product-id]').data('product-id'));
                  });
                  $input.data('update_change', true);

                  ajax.jsonRpc("/shop/cart/update_json", 'call', {
                      'line_id': line_id,
                      'product_id': parseInt($input.data('product-id'), 10),
                      'set_qty': value
                  }).then(function (data) {
                      var $closest_order = $input.closest('.js_cart_lines');

                      $closest_order.next('.js_cart_lines').first().remove() //to make previous total price row blank
                      $closest_order.next('.js_cart_lines').first().remove()
                      $closest_order.next('.js_cart_lines').first().remove()

                      if (data.no_line){
                          $input.closest('.panel').remove();
                      }

                      $input.data('update_change', false);
                      if (value !== parseInt($input.val() || 0, 10)) {
                          $input.trigger('change');
                          return;
                      }
                      var $q = $(".my_cart_quantity");
                      if (data.total_cart_qty) {
                          $q.parents('li:first').removeClass("hidden");
                      }
                      else {
                          $q.parents('li:first').addClass("hidden");
                          $('a[href^="/shop/checkout"]').addClass("hidden");
                      }

                      $q.html(data.total_cart_qty).hide().fadeIn(600);
                      $input.val(data.quantity);
                      $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                      if (data.total_cart_qty < 1){
                          $('.oe_cart').first().append("<div class='js_cart_lines well well-lg'>Your cart is empty!</div>")
                        //   <h2 class='mb8 mt8 text-primary'>Shopping Cart</h2>\
                        //   <a href='/shop' class='btn btn-default mb16'>\
                        //       <span class='fa fa-long-arrow-left' />\
                        //       <span class='hidden-xs'>Continue Shopping</span>\
                        //       <span class='visible-xs-inline'>Continue</span>\
                        //   </a>
                      }
                      $closest_order.prev('.js_cart_lines').remove();
                      $closest_order.prev('.js_cart_lines').remove();
                      $closest_order.replaceWith(data['website_sale.cart_lines'])

                    //   $closest_order.first().before(data['website_sale.cart_lines']).end().remove();

                      if (data.warning) {
                          var cart_alert = $('.oe_cart').parent().find('#data_warning');
                          if (cart_alert.length === 0) {
                              $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                                      '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                          }
                          else {
                              cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                          }
                          $input.val(data.quantity);
                      }
                  });
                }, 500);
            });
        })

        $('a[href*="/shop/checkout"]').on("click", function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var href = $(this).attr('href')
            var seller = href.substring((href.indexOf('seller=')-1)) // this gives ?seller=51
            var seller_id = seller.slice(seller.indexOf('=') + 1).split('&')[0];
            if (seller != seller_id){
                seller_id= parseInt(seller_id)
            }
            ajax.jsonRpc('/seller/wise/checkout', 'call', {
                'seller_id': seller_id,
            }).done(function(res) {
              window.location.href = '/shop/checkout';
            });
        });


        // accordion code

        // Add minus icon for collapse element which is open by default
        $(".collapse.in").each(function(){
            $(this).siblings(".panel-heading").find(".mp_checkout_accordian").addClass("fa-minus").removeClass("fa-plus");
            // $(this).parent().addClass("panel-primary");
        });

        // Toggle plus minus icon on show hide of collapse element
        $(".collapse").on('show.bs.collapse', function(){
            $(this).parent().find(".mp_checkout_accordian").removeClass("fa-plus").addClass("fa-minus");
            $(this).parent().addClass("panel-primary").removeClass("panel-default");
        }).on('hide.bs.collapse', function(){
        	$(this).parent().find(".mp_checkout_accordian").removeClass("fa-minus").addClass("fa-plus");
            $(this).parent().addClass("panel-default").removeClass("panel-primary");
        });

        $('body').on("click",'a[href*="/shop/cart"][class*="btn-primary"]', function(ev) {
            var href = $(this).attr('href')
            var element = href.split("#")[1]
            $(document.getElementById(element))
                .addClass('panel-primary')
                .removeClass("panel-default")
                .find(".mp_checkout_accordian")
                .removeClass("fa-plus")
                .addClass("fa-minus");
            $(document.getElementById(element))
                .siblings(".panel")
                .addClass("panel-default")
                .removeClass("panel-primary")
                .find(".mp_checkout_accordian")
                .removeClass("fa-minus")
                .addClass("fa-plus");
            var open_panel = element.split("_")[1]
            $(document.getElementById(open_panel)).addClass('in')
            $(document.getElementById(element)).siblings(".panel").children('.panel-body').removeClass("in")
        })


    })

})
