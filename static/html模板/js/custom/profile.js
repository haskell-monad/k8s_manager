/*
 * 	Additional function for profile.html
 *	Written by ThemePixels	
 *	http://themepixels.com/
 *
 *	Copyright (c) 2012 ThemePixels (http://themepixels.com)
 *	
 *	Built for Amanda Premium Responsive Admin Template
 *  http://themeforest.net/category/site-templates/admin-templates
 */

jQuery(document).ready(function(){
								
	jQuery('#followbtn').click(function(){
		if(jQuery(this).text() == 'Follow') {
			jQuery(this).text('Following')
						.removeClass('btn_yellow')
						.addClass('btn_lime');
			
			//this is an example of updating number 
			//of following when clicking follow button
			jQuery('#following span').text('21');
			
			//use the line of code below to implement it to the server using ajax
			//uncomment the code to use it
			//var action = 'Follow';
			//var url = 'enter your url here'
			//jQuery.post(url,{action: action},function(data) {
				//the server response should be the updated number of following
			//});
			
		} else {
			jQuery(this).text('Follow')
						.removeClass('btn_lime')
						.addClass('btn_yellow');
			
			//this is an example of updating number 
			//of following when clicking following button
			jQuery('#following span').text('20'); 
			
			//use the line of code below to implement it to the server using ajax
			//uncomment the code to use it
			//var action = 'Unfollow';
			//var url = 'enter your url here'
			//jQuery.post(url,{action: action},function(data) {
				//the server response should be the updated number of following
			//});
		}
	});
	
	///// ACTIVE STATUS ON HOVER /////
	jQuery('.bq2').hover(function(){
		jQuery(this).find('.edit_status').show();	
	},function(){
		jQuery(this).find('.edit_status').hide();	
	});
	
	
	///// CONTENT SLIDER /////
	jQuery('#slidercontent').bxSlider({
		prevText: '',
		nextText: ''
	});
	

	///// AUTOGROW TEXTAREA /////
	jQuery('#comment').autogrow();


	
	
});
