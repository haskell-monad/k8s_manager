

function flushHtmlByAjax(url,tagId,_callback){
	jQuery.ajax({
		  url: url,
		  type: 'get',
		  dataType: 'html',
		  success: function (data, status) {
			jQuery("#"+tagId).html(data);
		 	if(typeof _callback === "function"){
		 		_callback();
		 	}
			
		  },
		  fail: function (err, status) {
			console.log("加载页面失败",url,err);
		  }
	})
}

//新增产品页面
function productAdd(){
	flushHtmlByAjax("/product/add","centerContent");
}

//编辑产品页面
function productEdit(id){
	flushHtmlByAjax("/product/edit/"+id,"centerContent");
}

//新增版本页面
function versionAdd(productId){
	flushHtmlByAjax("/product/version/add/"+productId,"centerContent");
}

//编辑版本页面
function versionEdit(id){
	flushHtmlByAjax("/product/version/edit/"+id,"centerContent");
}

//新增资产页面
function assetsAdd(){
	flushHtmlByAjax("/assets/add","centerContent");
}

//编辑资产页面
function assetsEdit(id){
	flushHtmlByAjax("/assets/edit/"+id,"centerContent");
}

//编辑服务器页面
function serverEdit(assetsId){
   flushHtmlByAjax("/assets/server/edit/"+assetsId,"centerContent");
}

//kubernetes
function k8sAdd(){
	 flushHtmlByAjax("/k8s/add","centerContent");
}

function k8sInstall(id){
	 flushHtmlByAjax("/k8s/install/"+id,"centerContent");
}


function line(){
		var line_num = jQuery(".form-line").length;
		console.log(line_num);
		return line_num;
}

function k8s_all_line_call(){
	jQuery('#add-line').on('click', function(){  
		console.log("-----");
		var num = line(); 

		jQuery("#form-body").append("<tr>aaa-"+num+"-bbb</tr>");
	});
}

function k8sClusterAdd(kube_id){
	flushHtmlByAjax("/k8s/cluster/add/"+kube_id,"centerContent");

}







