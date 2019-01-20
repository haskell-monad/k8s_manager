

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

//添加kubernetes集群页面
function k8sAdd(){
	 flushHtmlByAjax("/k8s/add","centerContent");
}

// 添加 安装验证 命令 手册
function installCheckAdd(){
	flushHtmlByAjax("/k8s/command/add","centerContent");
}

// 安装验证命令 列表
function installCheckList(){
	flushHtmlByAjax("/k8s/command/list","centerContent");
}

// 编辑验证命令 
function installCheckEdit(command_id){
	flushHtmlByAjax("/k8s/command/edit/"+command_id,"centerContent");
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

function request_by_ajax(_url,_callback){
	jQuery.ajax({
		  url: _url,
		  type: 'get',
		  dataType: 'html',
		  success: function (data) {
		  	console.log("request_by_ajax",data);
		 	if(typeof _callback === "function"){
		 		_callback(data);
		 	}
		  },
		  fail: function (err, status) {
			console.log("request_by_ajax失败",url,err);
		  }
	})
}

// 执行集群部署命令
function k8s_install_command(kube_id,step_id){
	request_by_ajax("/k8s/install/command/"+kube_id+"/"+step_id,show_msg);
}

// 执行集群部署检测命令
function k8s_check_command(kube_id,command_id){
	request_by_ajax("/k8s/check/command/"+kube_id+"/"+command_id,show_msg);
}

function alert_msg(msg){
	alert(msg)
}

// 删除k8s集群节点
function k8s_remove_node(kube_id,node_id){
	request_by_ajax("/k8s/remove/node/"+kube_id+"/"+node_id,alert_msg);
}




