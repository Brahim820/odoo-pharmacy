/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('marketplace_pharmacist_details.mp_pharmacist_details', function (require) {

    var core = require('web.core');
    var ajax = require('web.ajax');


    $(document).ready(function() {

            $('.comm_reg_browse_btn').click(function(e){
                $('#comm_reg').trigger('click');
            });

            $('input[type="file"][name="comm_reg"]'). change(function(e){
                var fileName = e.target.files[0].name;
                $("#comm_reg_file_name").text(fileName)
            });

            $('input[type="file"][name="tax_card"]'). change(function(e){
                var fileName = e.target.files[0].name;
                $("#tax_card_file_name").text(fileName)
            });

            $('.tax_card_browse_btn').click(function(){
                $('#tax_card').trigger('click');
            });

            $('#pharmacy_form_submit').on('click', function(event){
                pharmacy_account_exist = $(this).data('pharmacy_account_exist')
                if (pharmacy_account_exist=="True"){
                    $(document).find(".pharmacy_account_exist").css("display","grid")
                    event.preventDefault();
                }

            })

    })

})
