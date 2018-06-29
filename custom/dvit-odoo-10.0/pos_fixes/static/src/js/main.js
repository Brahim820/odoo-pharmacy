odoo.define("pos_fixes", function(require) {
	"use strict";
	var Screens = require("point_of_sale.screens");
	Screens.ScreenWidget.include({
		barcode_product_action: function(code){
			if ($(".payment-screen").hasClass("oe_hidden")) {
				var self = this;
		        if (self.pos.scan_product(code)) {
		            if (self.barcode_product_screen) {
		                self.gui.show_screen(self.barcode_product_screen, null, null, true);
		            }
		        } else {
		            this.barcode_error_action(code);
		        }
			}else{
				return undefined;
			}
		}
	});
});
