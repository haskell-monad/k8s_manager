var node_type_color = ["","#EEDC82","#EEA9B8","#EED5B7","#B3B3B3"];
var node_role_color = ["","#4EEE94","#BFEFFF"];

jQuery(document).ready(function(){

	jQuery('#add-line').on('click', function(){  
    	jQuery(".form-body").append(copy_line());

	});

	jQuery('#del-line').on('click', function(){  
    	if(parseInt(data_line()) <= parseInt(jQuery(this).attr("value"))){
    		return;
    	}
    	jQuery(".form-body").children("tr:last").remove();
	});

	jQuery(document).on('change','.css-node-type',function(){
		jQuery(this).parents('tr').css('background-color', node_type_color[jQuery(this).prop('selectedIndex')]);
	});

	jQuery(document).on('change','.css-node-role',function(){
		jQuery(this).css('background-color', node_role_color[jQuery(this).prop('selectedIndex')]);
	});

});

function data_line(){
		return jQuery(".form-line").length;
}

function copy_line(){
	var html = jQuery(".form-line:first").clone().html().replace(/\s\r\n/g,"").replace(/form\-0/g,"form\-"+data_line());
	return '<tr class="gradeX form-line">'+html+'</tr>';
}