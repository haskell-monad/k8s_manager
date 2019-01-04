/*
 * 	Additional function for elements.html
 *	Written by ThemePixels	
 *	http://themepixels.com/
 *
 *	Copyright (c) 2012 ThemePixels (http://themepixels.com)
 *	
 *	Built for Amanda Premium Responsive Admin Template
 *  http://themeforest.net/category/site-templates/admin-templates
 */

jQuery(document).ready(function(){

	
	///// COLOR PICKER /////
	jQuery('#colorpicker').ColorPicker({
		onSubmit: function(hsb, hex, rgb, el) {
			jQuery(el).val('#'+hex);
			jQuery(el).ColorPickerHide();
		},
		onBeforeShow: function () {
			jQuery(this).ColorPickerSetColor(this.value);
		}
	})
	.bind('keyup', function(){
		jQuery(this).ColorPickerSetColor(this.value);
	});
	
	
	///// COLOR PICKER 2 /////
	jQuery('#colorSelector').ColorPicker({
		onShow: function (colpkr) {
			jQuery(colpkr).fadeIn(500);
			return false;
		},
		onHide: function (colpkr) {
			jQuery(colpkr).fadeOut(500);
			return false;
		},
		onChange: function (hsb, hex, rgb) {
			jQuery('#colorSelector span').css('backgroundColor', '#' + hex);
			jQuery('#colorpicker2').val('#'+hex);
		}
	});
	
	
	///// COLOR PICKER FLAT MODE /////
	jQuery('#colorpickerholder').ColorPicker({
		flat: true,
		onChange: function (hsb, hex, rgb) {
			jQuery('#colorpicker3').val('#'+hex);
		}
	});
	
	
	////// SLIDER ///// 
	jQuery("#slider").slider({value: 40});
	
	///// SLIDER SNAP TO INCREMENTS /////
	jQuery("#slider2").slider({
			value:100,
			min: 0,
			max: 500,
			step: 50,
			slide: function(event, ui) {
				jQuery("#amount").text("$"+ui.value);
			}
	});
	jQuery("#amount").text("$" + jQuery("#slider").slider("value"));

	
	///// SLIDER WITH RANGE /////
	jQuery("#slider3").slider({
		range: true,
		min: 0,
		max: 500,
		values: [ 75, 300 ],
		slide: function( event, ui ) {
			jQuery("#amount2").text("$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ]);
		}
	});
	jQuery("#amount2").text("$" + jQuery("#slider3").slider("values", 0) +
			" - $" + jQuery("#slider3").slider("values", 1));
	
	
	///// SLIDER WITH FIXED MINIMUM /////
	jQuery("#slider4").slider({
			range: "min",
			value: 37,
			min: 1,
			max: 100,
			slide: function( event, ui ) {
				jQuery("#amount4").text("$" + ui.value);
			}
	});
	jQuery("#amount4").text("$"+jQuery("#slider4").slider("value"));

	
	///// SLIDER WITH FIXED MAXIMUM /////
	jQuery("#slider5").slider({
			range: "max",
			value: 60,
			min: 1,
			max: 100,
			slide: function(event, ui) {
				jQuery("#amount5").text("$"+ui.value);
			}
	});
	jQuery("#amount5").text("$"+jQuery("#slider5").slider("value"));
	
	
	///// SLIDER VERTICAL /////
	jQuery("#slider6").slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 100,
			value: 60,
			slide: function( event, ui ) {
				jQuery("#amount6").text(ui.value);
			}
	});
	jQuery("#amount6").text( jQuery("#slider6").slider("value"));

	
	///// SLIDER VERTICAL WITH RANGE /////
	jQuery("#slider7").slider({
			orientation: "vertical",
			range: true,
			values: [17, 67],
			slide: function(event, ui) {
				jQuery("#amount7").text("$"+ui.values[0]+"-$"+ui.values[1]);
			}
		});
	jQuery("#amount7").text("$"+jQuery("#slider7").slider("values",0) +
			" - $"+jQuery("#slider7").slider("values",1));
	
	
	////// GROWL NOTIFICATION /////
	jQuery('.growl').click(function(){
		jQuery.jGrowl("Hello world!");
		return false;
	});
	
	jQuery('.growl2').click(function(){
		var msg = "This notification will live a little longer.";
		var position = "center";
		var scrollpos = jQuery(document).scrollTop();
		if(scrollpos < 50) position = "customtop-right";
		jQuery.jGrowl(msg, { life: 5000, position: position});
		return false;
	});
	
	//this will prevent growl box to show on top of the header when
	//scroll event is fired
	jQuery(document).scroll(function(){
		if(jQuery('.jGrowl').length != 0) {
			var pos = jQuery(document).scrollTop();
			if(pos < 50) jQuery('.jGrowl').css({top: '55px'}); else jQuery('.jGrowl').css({top: '0'});
		}
	});
	
	///// SAMPLE OF BUTTON ANIMATION UPON HOVER /////
	jQuery('.anchorbutton').hover(function(){
		jQuery(this).stop().animate({
			backgroundColor: '#FB9337', 
			borderColor: '#F0882C', 
			color: '#fff'
		},500);
	},function(){
		jQuery(this).stop().animate({
			backgroundColor: '#f7f7f7',
			borderColor: '#ddd',
			color: '#666'
		},300);
	});
	
	///// MODAL ALERT BOXES /////
	jQuery('.alertboxbutton').click(function(){
		jAlert('This is a custom alert box', 'Alert Dialog');
		return false;
	});
	
	jQuery('.confirmbutton').click(function(){
		jConfirm('Can you confirm this?', 'Confirmation Dialog', function(r) {
			jAlert('Confirmed: ' + r, 'Confirmation Results');
		});
		return false;
	});
	
	jQuery('.promptbutton').click
	(function(){
		jPrompt('Type something:', 'Prefilled value', 'Prompt Dialog', function(r) {
			if( r ) alert('You entered ' + r);
		});
		return false;
	});
	
	jQuery('.alerthtmlbutton').click(function(){
		jAlert('You can use HTML, such as <strong>bold</strong>, <em>italics</em>, and <u>underline</u>!');
		return false;
	});
	
	
	///// PAGINATION /////
	jQuery('.pagination').each(function(){
										
		var pa = jQuery(this);
		
		pa.find('a').click(function(){
			var p = jQuery(this).parent();
			if(!p.hasClass('previous') && !p.hasClass('first') && !p.hasClass('next') && !p.hasClass('last')) {
				pa.find('a').each(function(){
					jQuery(this).removeClass('current');
				});
				jQuery(this).addClass('current');
				
				//disable next and last button when active page is the last page
				if(jQuery(this).parent().next().hasClass('next')) {
					pa.find('.next a').addClass('disable');
					pa.find('.last a').addClass('disable');
				} else {
					pa.find('.next a').removeClass('disable');
					pa.find('.last a').removeClass('disable');
				}
				
				//disable first and previous button when active page is the first page
				if(jQuery(this).parent().prev().hasClass('previous')) {
					pa.find('.previous a').addClass('disable');
					pa.find('.first a').addClass('disable');
				} else {
					pa.find('.previous a').removeClass('disable');
					pa.find('.first a').removeClass('disable');
				}
				
			}
			return false;
		});
		
		
		///// CLICKING NEXT BUTTON /////
		pa.find('li.next a').click(function(){
			if(!jQuery(this).hasClass('disable')) {
				if(!jQuery(this).parent().prev().find('a').hasClass('current')) {
					pa.find('a.current').removeClass('current').parent().next().find('a').addClass('current');
				}
			}
			if(pa.find('a.current').parent().next().hasClass('next')) {
				pa.find('.next a').addClass('disable');
				pa.find('.last a').addClass('disable');
			}
			if(!pa.find('a.current').parent().prev().hasClass('previous')) {
				pa.find('.previous a').removeClass('disable');
				pa.find('.first a').removeClass('disable');
			}
	
		});
		
		
		///// CLICKING PREVIOUS BUTTON /////
		pa.find('li.previous a').click(function(){
			if(!jQuery(this).hasClass('disable')) {
				if(!jQuery(this).parent().next().find('a').hasClass('current')) {
					pa.find('a.current').removeClass('current').parent().prev().find('a').addClass('current');
				}
			}
			if(pa.find('a.current').parent().prev().hasClass('previous')) {
				pa.find('.first a').addClass('disable');
				pa.find('.previous a').addClass('disable');	
			}
			if(!pa.find('a.current').parent().next().hasClass('next')) {
				pa.find('.next a').removeClass('disable');
				pa.find('.last a').removeClass('disable');
			}
	
		});
		
		
		//// CLICKING LAST BUTTON /////
		pa.find('.last a').click(function(){
			jQuery(this).addClass('disable');
			pa.find('.next a').addClass('disable');
			pa.find('.current').removeClass('current');
			pa.find('.next a').parent().prev().find('a').addClass('current');
			pa.find('.first a, .previous a').removeClass('disable');
		});
		
		///// CLICKING FIRST BUTTON /////
		pa.find('.first a').click(function(){
			jQuery(this).addClass('disable');
			pa.find('.previous a').addClass('disable');
			pa.find('.current').removeClass('current');
			pa.find('.previous a').parent().next().find('a').addClass('current');
			pa.find('.last a, .next a').removeClass('disable');
		});

		
		
	});
		
	
	///// SHOW TAB WIDGET /////
	jQuery('#tabs').tabs();
	
	///// DATE PICKER /////
	jQuery( "#datepicker" ).datepicker();
	
	///// SORTABLE ITEM /////
	jQuery("#sortable, #sortable2").sortable();
	
	///// SORTABLE ITEM WITH DETAILS /////
	jQuery('.arrowdrop').click(function(){
		var t = jQuery(this);
		var det = t.parents('li').find('.details');
		if(!det.is(':visible')) {
			det.slideDown();
			t.addClass('arrowup');
		} else {
			det.slideUp();
			t.removeClass('arrowup');
		}
	});


});