/*
 * 	Additional function for support.html
 *	Written by ThemePixels	
 *	http://themepixels.com/
 *
 *	Copyright (c) 2012 ThemePixels (http://themepixels.com)
 *	
 *	Built for Amanda Premium Responsive Admin Template
 *  http://themeforest.net/category/site-templates/admin-templates
 */

jQuery(document).ready(function(){

	///// SEARCH USER FROM RIGHT SIDEBAR /////
	jQuery('.chatsearch input').bind('focusin focusout',function(e){
		if(e.type == 'focusin') {
			if(jQuery(this).val() == 'Search') jQuery(this).val('');	
		} else {
			if(jQuery(this).val() == '') jQuery(this).val('Search');	
		}
	});
	
	///// SUBMIT A MESSAGE VIA A SUBMIT BUTTON CLICK /////
	jQuery('.messagebox button').click(function(){
		enterMessage();
	});
	
	///// SUBMIT A MESSAGE VIA AN ENTER KEY PRESS /////
	jQuery('.messagebox input').keypress(function(e){
		if(e.which == 13)
			enterMessage();
	});
	
	function enterMessage() {
		var msg = jQuery('.messagebox input').val(); //get the value of message box
		
		//display message from a message box
		if(msg != '') {
			jQuery('#chatmessageinner').append('<p><img src="images/thumbs/avatar12.png" alt="" />'
											   +'<span class="msgblock radius2"><strong>You</strong> <span class="time">- 10:14 am</span>'
											   +'<span class="msg">'+msg+'</span></span></p>');
			jQuery('.messagebox input').val('');
			jQuery('.messagebox input').focus();
			jQuery('#chatmessageinner').animate({scrollTop: jQuery('#chatmessageinner').height()});
			
			//this will create a sample response display after submitting message
			window.setTimeout(  
				function() {  
					//this is just a sample reply when somebody send a message
					jQuery('#chatmessageinner').append('<p class="reply"><img src="images/thumbs/avatar13.png" alt="" />'
													   +'<span class="msgblock radius2"><strong>Tigress:</strong> <span class="time">10:15 am</span>'
													   +'<span class="msg">This is an automated reply!!</span></span></p>', function(){
						jQuery(this).animate({scrollTop: jQuery(this).height()});
					});
				}, 1000);			
		}	
	}
	
});
