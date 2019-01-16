

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


function k8sClusterAdd(kube_id){
	flushHtmlByAjax("/k8s/cluster/add/"+kube_id,"centerContent");

}

// 显示消息
function show_msg(msg){

	jQuery("#reply").append("<span class=\"msg\">"+msg+"</span>");
}

function request_by_ajax(kube_id,step_id,_callback){
	jQuery.ajax({
		  url: "/k8s/install/command/"+kube_id+"/"+step_id,
		  type: 'get',
		  dataType: 'html',
		  success: function (data, status) {
		  	console.log("request_by_ajax",data);
			show_msg(data);
		 	if(typeof _callback === "function"){
		 		_callback();
		 	}
		  },
		  fail: function (err, status) {
			console.log("request_by_ajax失败",url,err);
		  }
	})
}


// 安装命令
function k8s_install_command(kube_id,step_id){

	request_by_ajax(kube_id,step_id);
}






