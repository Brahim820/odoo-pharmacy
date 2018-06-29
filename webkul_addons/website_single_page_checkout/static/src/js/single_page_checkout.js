odoo.define('website_single_page_checkout.website_single_page_checkout', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    $(document).ready(function() {

        $("#add_new_address").on('click', function (ev) {
            $("#signle_page_checkout_address, #add_new_address, .show_all_shipping, .all_shipping").toggle();
            $("input[name='is_new_address']").prop('value', true);
            $(".oe_sale_acquirer_button").addClass("disabled_payment_div");
            $(".wk_has_error input").val("").prop("disabled", false);
            $(".wk_has_error input, select").prop("disabled", false);
            $("#save_selected").hide();
            var save_address = $("#save_address");
            save_address.show();
            save_address.removeClass("disabled");
            // $("#save_address").removeClass("disabled");
            save_address.find("span.fa").removeClass("fa-spinner fa-pulse");
            save_address.find("span.fa").addClass("fa-long-arrow-right ");
        });
        
        $(".show_all_shipping").on('click', function (ev) {
            $("#signle_page_checkout_address, .show_all_shipping, #add_new_address, .all_shipping").toggle();
            $("input[name='is_new_address']").prop('value', false);
            $(".oe_sale_acquirer_button").removeClass("disabled_payment_div");
            $(".all_shipping").find(".one_kanban").find("div.border_primary").find("a.btn-default").click();
        });

        $("#save_address").on('click', function (ev) {
            var self = this;
            var wk_div_name = $("input[name='wk_name']").val();
            var wk_div_email = $("input[name='wk_email']").val();
            var wk_div_phone = $("input[name='wk_phone']").val();
            var wk_div_street = $("input[name='wk_street']").val();
            var wk_div_city = $("input[name='wk_city']").val();
            var wk_div_zip = $("input[name='wk_zip']").val();
            var wk_div_country = $("#country_id").val();
            var wk_div_state = $("#wk_state_id").val()
            var is_state_visible = $("#wk_state_id").is(":visible");

            if (!wk_div_name) {
                $("#wk_div_name").addClass("has-error");
            }
            else{
                $("#wk_div_name").removeClass("has-error");
            }
            if (!wk_div_email) {
                $("#wk_div_email").addClass("has-error");
            }
            else{
                $("#wk_div_email").removeClass("has-error");
            }
            if (!wk_div_phone) {
                $("#wk_div_phone").addClass("has-error");
            }
            else{
                $("#wk_div_phone").removeClass("has-error");
            }
            if (!wk_div_street) {
                $("#wk_div_street").addClass("has-error");
            }
            else{
                $("#wk_div_street").removeClass("has-error");
            }
            if (!wk_div_city) {
                $("#wk_div_city").addClass("has-error");
            }
            else{
                $("#wk_div_city").removeClass("has-error");
            }
            if (!wk_div_country) {
                $("#wk_div_country").addClass("has-error");
            }
            else{
                $("#wk_div_country").removeClass("has-error");
            }
            if (!wk_div_state) {
                $("#wk_div_state").addClass("has-error");
            }
            else{
                $("#wk_div_state").removeClass("has-error");
            }
            if (wk_div_name && wk_div_email && wk_div_phone && wk_div_street && wk_div_city && wk_div_country && (is_state_visible ? wk_div_state : true ) ){
                $('#signle_page_checkout_address div').removeClass("has-error");
                $(this).addClass("disabled");
                $(this).find("span.fa").removeClass("fa-long-arrow-right ");
                $(this).find("span.fa").addClass("fa-spinner fa-pulse");
                ajax.jsonRpc('/save_address', 'call', {
                        'wk_name' : wk_div_name,
                        'wk_email' : wk_div_email,
                        'wk_phone' : wk_div_phone,
                        'wk_street' : wk_div_street,
                        'wk_city': wk_div_city,
                        "wk_zip": wk_div_zip,
                        'wk_country' : wk_div_country,
                        'wk_state' : wk_div_state,
                }).done(function (result) {
                    if (result) {
                        $(self).toggle();
                        $(".disabled_payment_div").removeClass("disabled_payment_div");
                        $(".wk_has_error input, select").prop('disabled', true);
                        $("#save_selected").toggle();
                        var $modal = $(result);
                        $(".all_shipping").find(".border_primary").removeClass("border_primary").addClass("js_change_shipping").find('.btn-ship').toggle();
                        $modal.insertBefore($(".all_shipping").find(".one_kanban").first());
                    } else {
                        console.log("else");
                        window.location.href = '/shop/checkout';
                    }
                }).fail(function (result) {
                    console.log(false);
                    window.location.href = '/shop/checkout';
                });
            }
        });
    });
});
