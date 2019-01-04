/*
 * 	Additional function for reports.html
 *	Written by ThemePixels	
 *	http://themepixels.com/
 *	
 *	Built for Amanda Premium Responsive Admin Template
 *  http://themeforest.net/category/site-templates/admin-templates
 */

jQuery(document).ready(function(){		
		
		
		/*****SIMPLE CHART*****/
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
		
		
		/*****BAR GRAPH*****/
		var d2 = [];
		for (var i = 0; i <= 10; i += 1)
			d2.push([i, parseInt(Math.random() * 30)]);
			
		var stack = 0, bars = true, lines = false, steps = false;
		jQuery.plot(jQuery("#bargraph"), [ d2 ], {
			series: {
				stack: stack,
				lines: { show: lines, fill: true, steps: steps },
				bars: { show: bars, barWidth: 0.6 }
			},
			grid: { hoverable: true, clickable: true, borderColor: '#ccc', borderWidth: 1, labelMargin: 10 },
			colors: ["#069"]
		});
		
		
		/**PIE CHART IN MAIN PAGE WHERE LABELS ARE INSIDE THE PIE CHART**/
		var data = [];
		var series = 5;
		for( var i = 0; i<series; i++) {
			data[i] = { label: "Series"+(i+1), data: Math.floor(Math.random()*100)+1 }
		}
		jQuery.plot(jQuery("#piechart"), data, {
				colors: ['#b9d6fd','#fdb5b5','#c9fdb5','#f9b5fd','#d7b5fd'],		   
				series: {
					pie: { show: true }
				}
		});
		
		
		/**ANOTHER PIE CHART IN MAIN PAGE WHERE LABELS ARER OUTSIDE THE PIE**/
		/*
		var data = [];
		var series = 5;
		for( var i = 0; i<series; i++) {
			data[i] = { label: "Series"+(i+1), data: Math.floor(Math.random()*100)+1 }
		}
		jQuery.plot(jQuery("#piechart2"), data, {
				colors: ['#ff7e00','#8aff00','#0096ff','#8400ff','#ff003c'],		   
				series: {
					pie: { show: true, radius: 1, label: { show: true, radius: 2/3, formatter: function(label, series){
                        return '<div class="pie">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
                    },
					threshold: 0.1,
                    background: { opacity: 0 }} }
				},
				legend: { show: false }
		});
		
		var data = [];
		var series = 5;
		for( var i = 0; i<series; i++) {
			data[i] = { label: "Series"+(i+1), data: Math.floor(Math.random()*100)+1 }
		}
		jQuery.plot(jQuery("#piechart3"), data, {
				colors: ['#c55c23','#8ac523','#2354c5','#8e23c5','#c52351'],		   
				series: {
					pie: { show: true }
				},
				legend: { show: false }
		});
		*/
		
		/***REAL TIME CHART***/
		// we use an inline data source in the example, usually data would
		// be fetched from a server
		var data = [], totalPoints = 300;
		function getRandomData() {
			if (data.length > 0)
				data = data.slice(1);
	
			// do a random walk
			while (data.length < totalPoints) {
				var prev = data.length > 0 ? data[data.length - 1] : 50;
				var y = prev + Math.random() * 10 - 5;
				if (y < 0)
					y = 0;
				if (y > 100)
					y = 100;
				data.push(y);
			}
	
			// zip the generated y values with the x values
			var res = [];
			for (var i = 0; i < data.length; ++i)
				res.push([i, data[i]])
			return res;
		}
	
		// setup control widget
		var updateInterval = 1000;
		jQuery("#updateInterval").val(updateInterval).change(function () {
			var v = jQuery(this).val();
			if (v && !isNaN(+v)) {
				updateInterval = +v;
				if (updateInterval < 1)
					updateInterval = 1;
				if (updateInterval > 2000)
					updateInterval = 2000;
				jQuery(this).val("" + updateInterval);
			}
		});
	
		// setup plot
		var options = {
			colors: ["#ffdd00"],
			series: { lines: { fill: true, fillColor: { colors: [ { opacity: 0.1 }, { opacity: 0.5 } ] } }, shadowSize: 0, }, // drawing is faster without shadows
			yaxis: { min: 0, max: 100 },
			grid: { borderColor: '#ccc', borderWidth: 1},
			
		};
		var plot = jQuery.plot(jQuery("#realtime"), [ getRandomData() ], options);
	
		function update() {
			plot.setData([ getRandomData() ]);
			// since the axes don't change, we don't need to call plot.setupGrid()
			plot.draw();
			
			setTimeout(update, updateInterval);
		}
	
		update();
	
		
		
});