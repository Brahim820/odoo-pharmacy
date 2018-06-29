odoo.define('theme_stoneware.front_js',function(require){
	'use strict';
  var animation = require('web_editor.snippets.animation');
  
  function initialize_owl(el){
   el.owlCarousel({
    items: 4,
            margin: 30,
            navigation: true,
            pagination: false,
            responsive: {
                0: {
                    items: 1,
                },
                481: {
                    items: 2,
                },
                768: {
                    items: 3,
                },
                1024: {
                    items: 4,
                }
            }

   })
  }
  function destory_owl(el){
    if(el && el.data('owlCarousel'))
   {
    el.data('owlCarousel').destroy();
    el.find('.owl-stage-outer').children().unwrap();
    el.removeData();
    }
  }
  animation.registry.advance_product_slider = animation.Class.extend({
    selector : ".tqt_products_slider",
        start: function (editMode) {
            var self = this;
			if (editMode)
            {$('.tqt_products_slider .advance_product_slider').addClass("hidden");
			}
			if(!editMode){
			var	tab_collection=parseInt(self.$target.attr('data-tab-id') || 0),
				slider_id='tqt_products_slider'+new Date().getTime();

            $.get("/shop/get_products_content",{'tab_id':self.$target.attr('data-tab-id') || 0,
												'slider_id':slider_id,

            									}).then(function( data ) {
                if(data){                   
                    self.$target.empty().append(data);
					$(".tqt_products_slider").removeClass('hidden');
					initialize_owl($(".tqt-pro-slide"));
    				
                }
            });
			}
        }
    });

    animation.registry.product_brand_slider = animation.Class.extend({
        selector: ".tqt_product_brand_slider",
        start: function(editable_mode) {
            var self = this;
            if (editable_mode) {
                $('.tqt_product_brand_slider .owl-carousel').empty();
            }
            if (!editable_mode) {
                $.get("/shop/get_product_brand_slider", {
                    'label': self.$target.attr('data-brand-label') || '',
                    'brand-count': self.$target.attr('data-brand-count') || 0,
                }).then(function(data) {
                    if (data) {
                    self.$target.empty().append(data);
					$(".tqt_product_brand_slider").removeClass('hidden');
					$.getScript("/theme_stoneware/static/src/js/owl.carousel.min.js");		
					$.getScript("/theme_stoneware/static/src/js/website.brand.js");												
					}
				});
			}
}
	});
});

