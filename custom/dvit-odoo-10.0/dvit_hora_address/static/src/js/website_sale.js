odoo.define('dvit_hora_address.website_sale', function(require) {
  "use strict";

  var ajax = require('web.ajax');
  require('website_sale.website_sale');

  if (!$('.oe_website_sale').length) {
    return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
  }

  $('.oe_website_sale').each(function() {
    var oe_website_sale = this;

    var clickwatch = (function() {
      var timer = 0;
      return function(callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
      };
    })();

    $(document).ready(function() {
        try {
            $("#delivery_date").datepicker({
                minDate: +0,
                maxDate: +2,
            });
        } catch (e) {}

        $('.btn-primary').bind("click", function(event) {
            var delivery_date = $('#delivery_date').val();
            var delivery_period = $('#delivery_period').val();
            if (delivery_date.length > 0 && delivery_period.length > 0){
              ajax.jsonRpc('/shop/delivery_date', 'call', {
                'delivery_date': delivery_date,
                'delivery_period': delivery_period
              });
              } else {
                event.stopPropagation();
                event.preventDefault();
                alert("Deliver date & time must be set!!");
            }
        });
    });

    if ($(".checkout_autoformat").length) {
      var selectStates = $("select[name='state_id']");
      var selectCities = $("select[name='city_id']");
      var selectZones = $("select[name='zone_id']");
      var selectBuilds = $("select[name='building_id']");
      selectStates.parent('div').hide();
      selectZones.parent('div').hide();
      selectBuilds.parent('div').hide();

      //states
      $(oe_website_sale).on('change', "select[name='state_id']", function() {
        clickwatch(function() {
          if ($("#state_id").val()) {
            ajax.jsonRpc("/shop/state_info/" + $("#state_id").val(), 'call').then(
              function(data) {
                var selectCities = $("select[name='city_id']");
                if (data.cities.length) {
                  selectCities.html('');
                  var opt = $('<option>').text('')
                    .attr('value', -1);
                  selectCities.append(opt);
                  _.each(data.cities, function(x) {
                    console.log('x is: ' + x);
                    var opt = $('<option>').text(x[1])
                      .attr('value', x[0]);
                    selectCities.append(opt);
                  });
                  selectCities.parent('div').show();
                } else {
                  selectCities.val(''); selectCities.parent('div').hide();
                  selectZones.val(''); selectZones.parent('div').hide();
                  selectBuilds.val(''); selectBuilds.parent('div').hide();
                }
                selectCities.data('init', 0);
              });
          }
        }, 500);
      });

      $("select[name='state_id']").change();

      //cities
      $(oe_website_sale).on('change', "select[name='city_id']", function() {
        clickwatch(function() {
          if ($("#city_id").val()) {
            ajax.jsonRpc("/shop/city_info/" + $("#city_id").val(), 'call').then(
              function(data) {
                var selectZones = $("select[name='zone_id']");
                if (data.zones.length) {
                  selectZones.html('');
                  var opt = $('<option>').text('')
                    .attr('value', -1);
                  selectZones.append(opt);
                  _.each(data.zones, function(x) {
                    console.log('x is: ' + x);
                    var opt = $('<option>').text(x[1])
                      .attr('value', x[0]);
                    selectZones.append(opt);
                  });
                  selectZones.parent('div').show();
                } else {
                  selectZones.val(''); selectZones.parent('div').hide();
                  selectBuilds.val(''); selectBuilds.parent('div').hide();
                }
                selectZones.data('init', 0);
              });
          }
        }, 500);
      });

      selectCities.change();

      //zones
      $(oe_website_sale).on('change', "select[name='zone_id']", function() {
        clickwatch(function() {
          if ($("#zone_id").val()) {
            ajax.jsonRpc("/shop/zone_info/" + $("#zone_id").val(), 'call').then(
              function(data) {
                // placeholder phone_code
                //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                var selectBuilds = $("select[name='building_id']");
                // dont reload state at first loading (done in qweb)
                // if (selectBuilds.data('init') === 0 || selectBuilds.find('option').length === 1) {
                if (data.builds.length) {
                  selectBuilds.html('');
                  var opt = $('<option>').text('')
                    .attr('value', -1);
                  selectBuilds.append(opt);
                  _.each(data.builds, function(x) {
                    console.log('x is: ' + x);
                    var opt = $('<option>').text(x[1])
                      .attr('value', x[0]);
                    selectBuilds.append(opt);
                  });
                  selectBuilds.parent('div').show();
                } else {
                  selectBuilds.val('');
                  selectBuilds.parent('div').hide();

                }
                selectBuilds.data('init', 0);
              });
          }
        }, 500);
      });

      selectZones.change();

    }
  });

});
