odoo.define('website_sale.editor', function (require) {
"use strict";

    require('website_sale.editor');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var options = require('web_editor.snippets.options');
    var _t = core._t;

    options.registry.website_sale = options.registry.website_sale.extend({
        start: function () {     
            var self = this;
            this.td_deal_id = parseInt(this.$target.attr("deal_id"));
            this._super();
          
        },
    reload: function () {
        if (location.href.match(/\?enable_editor/)) {
            location.reload();
        } else {
            location.href = location.href.replace(/\?(enable_editor=1&)?|#.*|$/, '?enable_editor=1&');
        }
    },
    bind_resize: function () {
        var self = this;
        this.$el.on('mouseenter', 'ul[name="size"] table', function (event) {
            $(event.currentTarget).addClass("oe_hover");
        });
        this.$el.on('mouseleave', 'ul[name="size"] table', function (event) {
            $(event.currentTarget).removeClass("oe_hover");
        });
        this.$el.on('mouseover', 'ul[name="size"] td', function (event) {
            var $td = $(event.currentTarget);
            var $table = $td.closest("table");
            var x = $td.index()+1;
            var y = $td.parent().index()+1;

            var tr = [];
            for (var yi=0; yi<y; yi++) tr.push("tr:eq("+yi+")");
            var $select_tr = $table.find(tr.join(","));
            var td = [];
            for (var xi=0; xi<x; xi++) td.push("td:eq("+xi+")");
            var $select_td = $select_tr.find(td.join(","));

            $table.find("td").removeClass("select");
            $select_td.addClass("select");
        });
        this.$el.on('click', 'ul[name="size"] td', function (event) {
            var $td = $(event.currentTarget);
            var x = $td.index()+1;
            var y = $td.parent().index()+1;
            ajax.jsonRpc('/shop/change_size', 'call', {'id': self.product_tmpl_id, 'x': x, 'y': y})
                .then(self.reload);
            ajax.jsonRpc('/deals/change_size', 'call', {'id': self.td_deal_id, 'x': x, 'y': y})
                .then(self.reload);
        });
    },
    /*style: function (type, value, $li) {
        if(type !== "click") return;
        ajax.jsonRpc('/deal/change_styles', 'call', {'id': this.td_deal_id, 'style_id': value});
    },*/
    go_to: function (type, value) {
        if(type !== "click") return;
        ajax.jsonRpc('/shop/change_sequence', 'call', {'id': this.product_tmpl_id, 'sequence': value})
            .then(this.reload);
        ajax.jsonRpc('/deal/change_sequence', 'call', {'id': this.td_deal_id, 'sequence': value})
            .then(this.reload);
    }
});
});
