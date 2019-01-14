var node_type_color = ["","#EEDC82","#EEA9B8","#EED5B7","#B3B3B3"];
var node_role_color = ["","#4EEE94","#BFEFFF"];

jQuery(document).ready(function(){

	jQuery('#add-line').on('click', function(){  
    	jQuery(".form-body").append(copy_line());
    	jQuery("#id_form-TOTAL_FORMS").val(parseInt(jQuery("#id_form-TOTAL_FORMS").val()) + 1);

	});

	jQuery('#del-line').on('click', function(){  
    	if(parseInt(data_line()) <= parseInt(jQuery(this).attr("value"))){
    		return;
    	}
    	jQuery(".form-body").children("tr:last").remove();
    	jQuery("#id_form-TOTAL_FORMS").val(parseInt(jQuery("#id_form-TOTAL_FORMS").val()) - 1);
	});
	jQuery("#set-line").on("click",function(){
		set_value(jQuery("#id_form-0-node_user").val(),"node_user");
		set_value(jQuery("#id_form-0-node_password").val(),"node_password");
		set_value(jQuery("#id_form-0-node_port").val(),"node_port");
	});

	jQuery(document).on('change','.css-node-type',function(){
		jQuery(this).parents('tr').css('background-color', node_type_color[jQuery(this).prop('selectedIndex')]);
	});

	jQuery(document).on('change','.css-node-role',function(){
		jQuery(this).css('background-color', node_role_color[jQuery(this).prop('selectedIndex')]);
	});

});

function set_value(new_value,select){
	if(new_value != null && new_value != ""){
		jQuery(".form-body [id *= \""+select+"\"]").each(function(i){
			if(jQuery(this).val() == null || jQuery(this).val() == ""){
				jQuery(this).val(new_value);	
			}
		});	
	}
}

function data_line(){
		return jQuery(".form-line").length;
}

function copy_line(){
	var html = jQuery(".form-line:first").clone().html().replace(/\s\r\n/g,"").replace(/form\-0/g,"form\-"+data_line());
	return '<tr class="gradeX form-line">'+html+'</tr>';
}