odoo.define('website_onepage_checkout.website_onepage_checkout', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');

    var _t = core._t;

    $(document).ready(function() {
        $('.oe_website_sale').each(function() {
            var oe_website_sale = this;

            $(oe_website_sale).on('click', '.submit-billing-btn', function(ev) {
                var shipping = $('#shipping-panel-data').data('shipping');
                if (shipping === 'off') {
                    confirm_order_details(oe_website_sale, 'billing-panel');
                } else {
                    success_panel('billing-panel');
                }
            });

            $(oe_website_sale).on('click', '.submit-shipping-btn', function(ev) {
                $('.oe_website_sale_onepage .has-error').removeClass('has-error');
                confirm_order_details(oe_website_sale, 'shipping-panel');
            });

            $(oe_website_sale).on('click', '.submit-extra-info-btn', function(e) {
                success_panel('extra-step-panel');
            });

            // when choosing an delivery carrier, update the total prices
            $(oe_website_sale).on('click', '.onepage_delivery', function(ev) {
                var carrierId = $(ev.currentTarget).val();
                $('.onepage-loader-big').show();
                ajax.jsonRpc('/shop/checkout/delivery_option', 'call', {
                        'carrier_id': carrierId
                    })
                    .done(function(result) {
                        if (result) {
                            if (result.success) {
                                set_order_amount(oe_website_sale, result);
                            } else {
                                error_panel('delivery-method-panel', '');
                            }
                        } else {
                            window.location.href = '/shop';
                        }
                        $('.onepage-loader-big').hide();
                    })
                    .fail(function(result) {
                        $('.onepage-loader-big').hide();
                        error_panel('delivery-method-panel', 'fail executed');
                    });
            });

            $(oe_website_sale).on('click', '.submit-delivery-btn', function(e) {
                success_panel('delivery-method-panel');
            });
        });

        function set_order_amount(oe_website_sale, result) {
            // order final total
            $('#order_total .oe_currency_value').text(result.order_total);
            $('#onepage_total .oe_currency_value').text(result.order_total);
            var total_ammount = (result.order_total).toString().replace(',', '');
            $(oe_website_sale).find('input[name="amount"]').val(total_ammount);

            // order tax amount
            $('#order_total_taxes .oe_currency_value').text(result.order_total_taxes);
            $('#onepage_taxes .oe_currency_value').text(result.order_total_taxes);

            // order total without tax and delivery
            $('#order_subtotal .oe_currency_value').text(result.order_subtotal);
            $('#onepage_subtotal .oe_currency_value').text(result.order_subtotal);

            // order delivery amount
            $('#order_delivery .oe_currency_value').text(result.order_total_delivery);
            $('#onepage_delivery .oe_currency_value').text(result.order_total_delivery);

        }

        function success_panel(panel_selector) {
            $('.' + panel_selector).attr('class', '').addClass('panel panel-success ' + panel_selector);
            $('.' + panel_selector).next().find('a.collapsed').removeClass('hide_class').trigger("click");
            $('.' + panel_selector).find('btn.btn-primary').show();
        }

        function error_panel(panel_selector, message) {
            $('.' + panel_selector).attr('class', '').addClass('panel panel-danger ' + panel_selector);
            $('.' + panel_selector).nextAll().find('a.collapsed').addClass('hide_class');
            $('.' + panel_selector).find('btn.btn-primary').hide();
            console.log(message);
        }

        function confirm_order_details(oe_website_sale, panel_selector) {
            $('.onepage-loader-big').show();
            ajax.jsonRpc('/shop/onepage/confirm_order', 'call', {})
            .done(function(result) {
                if (result[0]) {
                    var $template = $(result[2]);
                    var error = $template.find('input[name="delivery-error"]').val();
                    if (error) {
                        $('button.submit-delivery-btn').hide();
                        // error_panel('delivery-method-panel', '');
                    } else {
                        $('button.submit-delivery-btn').show();
                    }
                    $('.delivery-method-panel .panel-body').html($template);

                    if (result[1].success) {
                        set_order_amount(oe_website_sale, result[1]);
                        success_panel(panel_selector);
                    } else {
                        error_panel(panel_selector, '');
                    }

                } else {
                    window.location.href = result[1];
                }
                $('.onepage-loader-big').hide();
            })
            .fail(function(result) {
                $('.onepage-loader-big').hide();
                error_panel('shipping-panel', 'fail executed');
            });
        }

        function get_post_fields_vals(elms, data) {
            elms.each(function(index) {
                data[$(this).attr('name')] = $(this).val();
            });
            return data;
        }
    });
});

/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* Responsible Developer:- Sunny Kumar Yadav */
