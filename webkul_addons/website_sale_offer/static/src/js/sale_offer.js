odoo.define('website_sale_offer.sale_offer', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    $(document).ready(function () {
        $('input[name="acquirer"]').on('change', function (e) {
            // var checked_radio = $('input[name="pm_id"]:checked');
            var payment_acquirer_id = $(this).next('span').attr("data-oe-id")
            var promo_code = $('#applied_sale_offer_code').text();
            if (!payment_acquirer_id){
                payment_acquirer_id = $(this).val()
            }
            if ($(this).is(':checked')){
                // console.log(payment_acquirer_id);
                if (payment_acquirer_id && promo_code ) {
                    ajax.jsonRpc("/apply/sale_offer", 'call', {
                        'payment_acquirer_id': parseInt(payment_acquirer_id),
                        'promo_code': promo_code,
                    }).then(function (result) {
                        if (result) {
                            // console.log(result);
                            // if payment offer applied then change global discount and total ammoun
                            var global_discount = $("#order_global_discount.span.oe_currency_value");
                            var amount_total = $("#order_total.span.oe_currency_value");
                            $("#order_global_discount span.oe_currency_value").text(result.global_discount);
                            $("#order_total span.oe_currency_value").text(result.amount_total);
                        }
                    })
                }
            }
        });
    });
});
