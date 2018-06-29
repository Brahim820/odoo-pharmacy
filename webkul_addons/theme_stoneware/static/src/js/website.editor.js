odoo.define('theme_stoneware.editor_js',function(require) {
'use strict';
var Model = require('web.Model');
var ajax = require('web.ajax');
var core = require('web.core');
var base = require('web_editor.base');
var web_editor = require('web_editor.editor');
var options = require('web_editor.snippets.options');
var snippet_editor = require('web_editor.snippet.editor');
var website = require('website.website');
    var qweb = core.qweb;
var _t = core._t;
	ajax.loadXML('/theme_stoneware/static/src/xml/change_progress.xml', qweb);
	ajax.loadXML('/theme_stoneware/static/src/xml/product_template.xml', qweb);
    options.registry.advance_product_slider = options.Class.extend({
		popup_template_id: "editor_new_product_slider_template",
		popup_title: _t("Select Collection"),
        product_slider_configure: function(type,value) {
            var self = this;
			if (type == "click" || type==undefined){
var def = website.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Collection"),
            'init': function (field) {
                return new Model('multitab.configure').call('name_search', ['', []], { context: base.get_context() });
            },
        });
        def.then(function (collection_id) {
            self.$target.attr("data-tab-id", collection_id);
            new Model('multitab.configure').call('read', [[parseInt(collection_id)]], { context: base.get_context() }).then(function (data){
                if(data && data[0] && data[0].name)
                {
                 self.$target.empty().append('<div class="container"><div class="advance_product_slider"><div class="col-md-12"><div class="seaction-head"><h1>'+ data[0].name +'</h1> </div></div></div></div>');   
                }
            });
            
        });
        	return def; 
		}
		else{
			return ;
		}            
        },

        drop_and_build_snippet: function() {
            var self = this;
            this._super();
            this.product_slider_configure().fail(function () {
                self.editor.on_remove();
            });
        },
	clean_for_save:function(){
	$(".tqt_products_slider").empty();
	},
    });

   options.registry.product_brand_slider = options.Class.extend({
        brand_slider_configure: function(type,value) {
            var self = this;
			if (type == "click" || type==undefined){
						self.$modal = $(qweb.render("theme_stoneware.brand_slider_block"));
						self.$modal.appendTo('body');
						self.$modal.modal();
						var $brand_count = self.$modal.find("#brand-count"),
						    $cancel = self.$modal.find("#cancel"),
						    $sub_data = self.$modal.find("#sub_data"),
						    $brand_label = self.$modal.find("#brand-label");
						    						
						    
						$sub_data.on('click', function() {
						    var type = '';
						    self.$target.attr("data-brand-count", $brand_count.val());
						    self.$target.attr("data-brand-label", $brand_label.val());					    						    
						        if ($brand_label.val()) {
						            type = $brand_label.val();
						        } else {
						            type = "Brands";
						        }              
						    self.$target.empty().append('<div class="container"><div class="shopper_brand_slider"><div class="col-md-12"><div class="seaction-head"><h1>' + type + '</h1> </div></div></div></div>');
						});
			}
			else{
			return;
			}
        },

        drop_and_build_snippet: function() {
            var self = this;
            this._super();
            this.brand_slider_configure().fail(function () {
                self.editor.on_remove();
            });
        },
	clean_for_save:function(){
	$(".tqt_product_brand_slider").empty();
	},
    });

   options.registry.tabslide = options.Class.extend({
    start : function () {
        var self = this;
        this._super();
        this.id = this.$target.attr("id");
        this.$inner = this.$target.find("div[class='tab-content']");
        this.$indicators = this.$target.find("ul[role='tablist']");
    },   	
    add_tab: function(type,value) {
        var self = this;
        if(type !== "click") return;
		if (type == "click" || type==undefined){
			var self = this;
    		var cycle = this.$inner.length;
    		var id=new Date().getTime();
    		this.$indicators.append('<li role="presentation"><a href="#'+id+'" aria-controls="profile" role="tab" data-toggle="tab">New Tab</a></li>');
			this.$inner.append('<div role="tabpanel" class="tab-pane" id="'+id+'">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. </div>')
		}
		else{
		return;
		}
    },
    remove_tab: function(type,value){
        var self = this;
        if(type !== "click") return;
		if (type == "click" || type==undefined){
			var self = this;
    		var cycle = this.$inner.length;
    		var $active_tab = this.$inner.find("div[class='tabpanel'].active ,div[class='tabpanel']").first();
    		var $active_content=this.$indicators.find('li.active',li.active).first()
    		$active_tab.remove();
    		$active_content.remove();
		}
		else{
		return;
		}    	
    },
    drop_and_build_snippet: function() {
        var self = this;
        this._super();
        this.id = "tab_slide_" + new Date().getTime();
        this.$target.attr("id", this.id);        
        this.add_tab().fail(function () {
            self.editor.on_remove();
        });
    },
    }); 
   options.registry.theme_progressbar = options.Class.extend({
    start : function () {
        var self = this;
        this._super();
        this.id = this.$target.attr("id");
    },   	
    change_progress: function(type,value) {
        var self = this;
        if(type !== "click") return;
		if (type == "click" || type==undefined){
			self.$modal = $(qweb.render("theme_stoneware.change_progress_modal"));
				self.$modal.appendTo('body');
				self.$modal.modal();
				var $progress_width = self.$modal.find("#progress-width"),
				$sub_data = self.$modal.find("#sub_data");				    									    
				$sub_data.on('click', function() {
			    var type = '';
			    //self.$target.attr("data-animation-width", $progress_width.val());
			    self.$target.attr('data-animate-width',$progress_width.val()+'%');
			    //self.$target.attr('style','width:'+$progress_width.val()+'%;');	
	    		});			
			}
		else{
		return;
		}
    
    },
    drop_and_build_snippet: function() {
        var self = this;
        this._super();       
        this.change_progress().fail(function () {
            self.editor.on_remove();
        });
    },
    }); 

options.registry.collapse.include({
    on_clone: function ($clone) {
        this._super($clone);
        var id1="my_tab_title"+new Date().getTime();
		var id2="my_tab_target"+new Date().getTime();
		$clone.find(' .panel-heading').attr("id", id1);
		$clone.find('.panel-heading').attr('data-target','#'+id2),
		$clone.find('.panel-collapse').attr("id", id2);
		$clone.find('.panel-collapse').attr("class", 'panel-collapse collapse');
    },
});
     
});

