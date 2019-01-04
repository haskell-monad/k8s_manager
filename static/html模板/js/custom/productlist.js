jQuery(document).ready(function(){
	
	///// PRODUCT DISPLAY INFO WHEN HOVERING THUMBNAILS /////
	jQuery('.prodlist li').hover(function(){
		jQuery(this).find('.contentinner').stop().animate({marginTop: 0});
	},function(){
		jQuery(this).find('.contentinner').stop().animate({marginTop: '132px'});
	});
	
	///// SWITCHING LIST FROM 3 COLUMNS TO 2 COLUMN LIST /////
	function rearrangelist() {
		if(jQuery(window).width() < 480) {
			if(jQuery('.prodlist li.one_half').length == 0) {
				var count = 0;
				jQuery('.prodlist li').removeAttr('class');
				jQuery('.prodlist li').each(function(){
					jQuery(this).addClass('one_half');
					if(count%2 != 0) jQuery(this).addClass('last');
					count++;
				});	
			}
			
			if(jQuery(window).width() < 400)
				jQuery('.prodlist li').removeAttr('class');
		
		} else {
			if(jQuery('.prodlist li.one_third').length == 0) {
				var count = 0;
				jQuery('.prodlist li').removeAttr('class');
				jQuery('.prodlist li').each(function(){
					jQuery(this).addClass('one_third');
					if(count == 2){
						jQuery(this).addClass('last');
						count = 0;
					} else {
						count++;
					}
				});	
			}
		}
	}
	
	rearrangelist();
	
	///// ON RESIZE WINDOW /////
	jQuery(window).resize(function(){
		rearrangelist();
	});
});
