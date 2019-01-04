jQuery(document).ready(function(){
	
		jQuery('#overviewselect, input:checkbox').uniform();
		
		///// DATE PICKER /////
		jQuery( "#datepickfrom, #datepickto" ).datepicker();
		
		///// SLIM SCROLL /////
		jQuery('#scroll1').slimscroll({
			color: '#666',
			size: '10px',
			width: 'auto',
			height: '175px'                  
		});
		
		///// ACCORDION /////
		jQuery('#accordion').accordion({autoHeight:  false});
	
		///// SIMPLE CHART /////
		var flash = [[0, 2], [1, 6], [2,3], [3, 8], [4, 5], [5, 13], [6, 8]];
		var html5 = [[0, 5], [1, 4], [2,4], [3, 1], [4, 9], [5, 10], [6, 13]];
			
		function showTooltip(x, y, contents) {
			jQuery('<div id="tooltip" class="tooltipflot">' + contents + '</div>').css( {
				position: 'absolute',
				display: 'none',
				top: y + 5,
				left: x + 5
			}).appendTo("body").fadeIn(200);
		}
	
			
		var plot = jQuery.plot(jQuery("#chartplace"),
			   [ { data: flash, label: "Flash(x)", color: "#069"}, { data: html5, label: "HTML5(x)", color: "#FF6600"} ], {
				   series: {
					   lines: { show: true, fill: true, fillColor: { colors: [ { opacity: 0.05 }, { opacity: 0.15 } ] } },
					   points: { show: true }
				   },
				   legend: { position: 'nw'},
				   grid: { hoverable: true, clickable: true, borderColor: '#ccc', borderWidth: 1, labelMargin: 10 },
				   yaxis: { min: 0, max: 15 }
				 });
		
		var previousPoint = null;
		jQuery("#chartplace").bind("plothover", function (event, pos, item) {
			jQuery("#x").text(pos.x.toFixed(2));
			jQuery("#y").text(pos.y.toFixed(2));
			
			if(item) {
				if (previousPoint != item.dataIndex) {
					previousPoint = item.dataIndex;
						
					jQuery("#tooltip").remove();
					var x = item.datapoint[0].toFixed(2),
					y = item.datapoint[1].toFixed(2);
						
					showTooltip(item.pageX, item.pageY,
									item.series.label + " of " + x + " = " + y);
				}
			
			} else {
			   jQuery("#tooltip").remove();
			   previousPoint = null;            
			}
		
		});
		
		jQuery("#chartplace").bind("plotclick", function (event, pos, item) {
			if (item) {
				jQuery("#clickdata").text("You clicked point " + item.dataIndex + " in " + item.series.label + ".");
				plot.highlight(item.series, item.datapoint);
			}
		});
		
		
	///// SWITCHING LIST FROM 3 COLUMNS TO 2 COLUMN LIST /////
	function rearrangeShortcuts() {
		if(jQuery(window).width() < 430) {
			if(jQuery('.shortcuts li.one_half').length == 0) {
				var count = 0;
				jQuery('.shortcuts li').removeAttr('class');
				jQuery('.shortcuts li').each(function(){
					jQuery(this).addClass('one_half');
					if(count%2 != 0) jQuery(this).addClass('last');
					count++;
				});	
			}
		} else {
			if(jQuery('.shortcuts li.one_half').length > 0) {
				jQuery('.shortcuts li').removeAttr('class');
			}
		}
	}
	
	rearrangeShortcuts();
	
	///// ON RESIZE WINDOW /////
	jQuery(window).resize(function(){
		rearrangeShortcuts();
	});


});
