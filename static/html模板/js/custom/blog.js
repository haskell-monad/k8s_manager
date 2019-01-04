/*
 * 	Additional function for manageblog.html
 *	Written by ThemePixels	
 *	http://themepixels.com/
 *
 *	Copyright (c) 2012 ThemePixels (http://themepixels.com)
 *	
 *	Built for Amanda Premium Responsive Admin Template
 *  http://themeforest.net/category/site-templates/admin-templates
 */


jQuery(document).ready(function(){

	///// load ajax/blog/allposts.html /////
	
	jQuery.post('ajax/blog/allposts.html', function(data){
		jQuery('#contentwrapper').html(data);
		jQuery('.stdtable input:checkbox').uniform();	//restyling checkbox
	});
	
	jQuery('.checkall, .checkall2').live('click',function(){
		if(!jQuery(this).is(':checked')) {
			checkbox(jQuery(this),false);	
		} else {
			checkbox(jQuery(this),true);
		}
	});
	
	function checkbox(t,v) {
		t.parents('table').find('input[type=checkbox]').each(function(){
			if(!jQuery(this).parents('tr').hasClass('togglerow')) {
				jQuery(this).attr('checked',v);
			}
			jQuery.uniform.update();
		});	
	}
	
	///// DELETE A SINGLE BLOG LIST /////
	
	jQuery('.stdtable .delete').live('click',function(){
		var p = jQuery(this).parents('tr');
		jConfirm('Are you sure you want to delete this post?', 'Delete Post', function(r) {
			if(r) {
				if(p.next().hasClass('togglerow'))
					p.next().remove();

				p.fadeOut(function(){
					jQuery(this).remove();
				});
			}
		});
	return false;
	});
	
	
	///// QUICK VIEW /////
	
	jQuery('.quickview').live('click', function(){
		var parent = jQuery(this).parents('tr');
		var parentTable = jQuery(this).parents('table');
		var url = jQuery(this).attr('href');
		jQuery.post(url,function(data){
			parent.after('<tr class="togglerow"><td colspan="5">'+data+'</td></tr>');
			parentTable.find('.togglerow').each(function(){
				jQuery(this).hide();
			});
			parent.next().show();
			
			jQuery('.quickedit-date, input:checkbox, input:radio').uniform(); //restyling select element

		});
		return false;
	});
	
	///// QUICK VIEW UPDATE BUTTON /////
	jQuery('.quickformbutton .update').live('click',function(){
		jQuery(this).parent().find('.loading').show();
		return false;
	});
	
	///// QUICK VIEW CANCEL BUTTONS /////
	jQuery('.quickformbutton .cancel').live('click', function(){
		jQuery(this).parents('tr.togglerow').remove();
		return false;
	});
		
		
	///// SWITCHING LIST FROM 3 COLUMNS TO 2 COLUMN LIST /////
	function shortenedTab() {
		if(jQuery(window).width() < 450) {
			if(!jQuery('.hornav').hasClass('shortened')) { //checked to prevent running multiple times when resizing windows
				jQuery('.hornav').addClass('shortened');
				jQuery('.hornav').append('<li class="more"><a>More</a><ul></ul></li>');
				var count = 0;
				jQuery('.hornav li').each(function(){
					if(count > 1) {
						if(!jQuery(this).hasClass('more'))
							jQuery('.hornav li.more ul').append(jQuery(this));
					}
					count++;
				});	
			}
		} else {
			if(jQuery('.hornav').hasClass('shortened')) { //checked to prevent running multiple times when resizing windows
				jQuery('.hornav').removeClass('shortened');
				
				jQuery('.hornav li.more ul li').each(function(){
					jQuery('.hornav').append(jQuery(this));
				});
				jQuery('.hornav li.more').remove();
			}
		}
	}
	
	///// MORE DROPDOWN MENU IN HORIZONTAL MENU /////
	jQuery('.hornav li.more > a').live('click',function(){
		if(!jQuery('.hornav li.more ul').is(':visible')) {												
			jQuery('.hornav li').removeClass('current');
			jQuery(this).parent().addClass('current');
			jQuery(this).parent().find('ul').show();
		} else {
			jQuery('.hornav li.more ul').hide();	
		}
	});
		
	
	shortenedTab();
	
	///// ON RESIZE WINDOW /////
	jQuery(window).resize(function(){
		shortenedTab();
	});

	
	
});