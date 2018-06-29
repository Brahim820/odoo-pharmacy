odoo.define('website_wishlist.website_wishlist', function(require) {
    "use strict";
    var ids;
    var ajax = require('web.ajax');
    $(document).ready(function() {
        $('.oe_website_sale').each(function(ev) {
            var oe_website_sale = this;
            check_wishlist_onload();
            $(oe_website_sale).on('change', function(ev) {
                var product_id = check_product_id();
                if ($.inArray(product_id, ids) != -1) {
                    added_to_wishlist();
                } else {
                    add_to_wishlist();
                }
            });

            $(oe_website_sale).on('click', 'a.add_to_wishlist', function(ev) {
                var product = check_product_id();
                ajax.jsonRpc('/wishlist/add_to_wishlist', 'call', {
                    'product': product,
                })
                .then(function(res) {
                    if (res > 0) {
                        ids.push(product.toString());
                        $('.my_wishlist_quantity').parent().parent().removeClass("hidden");
                        $('.my_wishlist_quantity').html(res).hide().fadeIn(600);
                    } else {
                        $('.my_wishlist_quantity').parent().parent().addClass("hidden");
                    }
                });
                added_to_wishlist();
            });

            $(oe_website_sale).on("click", "a.remove_whishlist", function(ev) {
                var product_id = $(this).attr("whishlist-id");
                var row = $(this).closest('tr');
                remove_wishlist_product(product_id, row);
            });

            $(oe_website_sale).on("click", "a#wishlist_to_cart", function(ev) {
                var product_id = parseInt($(this).attr("product-id"), 10);
                var row = $(this).closest('tr');
                var value = 1;
                var $input = $(this);
                if ($input.data('update_change')) {
                    return;
                }
                ajax.jsonRpc("/shop/cart/update_json", 'call', {
                    'line_id': NaN,
                    'product_id': product_id,
                    'add_qty': value
                })
                .then(function(data) {
                    remove_wishlist_product(product_id, row);
                    $input.data('update_change', false);
                    if (value !== 1) {
                        $input.trigger('change');
                        return;
                    }
                    var $q = $(".my_cart_quantity");
                    if (data.cart_quantity) {
                        $q.parent().parent().removeClass("hidden");
                    } else {
                        $q.parent().parent().addClass("hidden");
                        $('a[href^="/shop/checkout"]').addClass("hidden")
                    }
                    $q.html(data.cart_quantity).hide().fadeIn(600);
                });
            });

            function remove_wishlist_product(product_id, row) {
                ajax.jsonRpc('/wishlist/remove_from_wishlist', 'call', {
                    'product': product_id,
                })
                .then(function(res) {
                    if (res > 0) {
                        $('.my_wishlist_quantity').parent().parent().removeClass("hidden");
                        $('.my_wishlist_quantity').html(res).hide().fadeIn(600);
                    } else {
                        $('.my_wishlist_quantity').parent().parent().addClass("hidden");
                    }
                });
                row.fadeOut(1000);
            }

            function check_wishlist_onload() {
                ids = $('#wishlist_ids').attr('ids');
                if (ids)
                    ids = ids.replace(/[\[\]']+/g, '').replace(/\s/g, '').split(',');
                else
                    ids = [];
                var product_id = check_product_id();
                if (product_id === '0') {
                    $("div.wishlist-box").hide();
                }
                if ($.inArray(product_id, ids) != -1) {
                    added_to_wishlist();
                } else {
                    add_to_wishlist();
                }
            }

            function check_product_id() {
                if ($("input[name='product_id']").is(':radio'))
                    var product_id = $("input[name='product_id']:checked").attr('value');
                else
                    var product_id = $("input[name='product_id']").attr('value');
                /* if not product if hide wishlist box */
                if (product_id === '0') {
                    $("div.wishlist-box").hide();
                } else {
                    $("div.wishlist-box").show();
                }
                return product_id
            }

            function added_to_wishlist() {
                $(".add_to_wishlist").html('Added to Wishlist');
                $(".add_to_wishlist").addClass('wishlist_disabled');
                $(".add_to_wishlist").parent().css("color","#990000");
            }

            function add_to_wishlist() {
                $(".add_to_wishlist").html(' Add to Wishlist');
                $(".add_to_wishlist").removeClass('wishlist_disabled');
                $(".add_to_wishlist").parent().css("color","black");
            }
        });
    });
});