odoo.define('website_sale.website_sale', function (require) {
"use strict";
$(document).ready(function() {
    $('.wk_deal').each(function (){
      if( $(this).attr("show_deal"))
      {
        var value =  $(this).attr("show_deal");
        if (value == 'blur')
        {
          console.log('inside');
          $(this).css( "opacity", 0.4 );
        }
        
      }
    });
    
    });
  }); 
  
