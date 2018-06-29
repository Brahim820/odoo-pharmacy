$(document).ready(function() {

var sync1 = $("#deals_slider");


       $(".deals-owl-carousel").each(function() {
        number = 10;

        $( this ).owlCarousel({     
        // singleItem : true,
        slideSpeed : 1000,
        navigation: true,
        pagination:false,
        afterAction : syncPosition,
        responsiveRefreshRate : 200,

        // "singleItem:true" is a shortcut for:
        items : 2, 
        itemsDesktop : false,
        itemsDesktopSmall : false,
        itemsTablet: false,
        itemsMobile : false,
       
        });

      });

      function syncPosition(el){
        var current = this.currentItem;

      }

      function center(number){
        var sync2visible = sync2.data("owlCarousel").owl.visibleItems;

        var num = number;
        var found = false;
        for(var i in sync2visible){
          if(num === sync2visible[i]){
            var found = true;
          }
        }

        if(found===false){
          if(num>sync2visible[sync2visible.length-1]){
            sync2.trigger("owl.goTo", num - sync2visible.length+2)
          }else{
            if(num - 1 === -1){
              num = 0;
            }
            sync2.trigger("owl.goTo", num);
          }
        } else if(num === sync2visible[sync2visible.length-1]){
          sync2.trigger("owl.goTo", sync2visible[1])
        } else if(num === sync2visible[0]){
          sync2.trigger("owl.goTo", num-1)
        }
      }

});