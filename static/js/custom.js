

function flushHtmlByAjax(url,tagId){
	jQuery.ajax({
		  url: url,
		  type: 'get',
		  dataType: 'html',
		  success: function (data, status) {
			jQuery("#"+tagId).html(data);
		  },
		  fail: function (err, status) {
			console.log("加载页面失败",url,err);
		  }
	})
}

//新增产品页面
function productAddPage(){
	flushHtmlByAjax("/product/addPage","centerContent");
}

//编辑产品页面
function productEditPage(id){
	flushHtmlByAjax("/product/editPage/"+id,"centerContent");
}

//新增版本页面
function versionAddPage(productId){
	flushHtmlByAjax("/product/version/addPage/"+productId,"centerContent");
}

//编辑版本页面
function versionEditPage(id){
	flushHtmlByAjax("/product/version/editPage/"+id,"centerContent");
}

//新增资产页面
function assetsAddPage(){
	flushHtmlByAjax("/assets/addPage","centerContent");
}

//编辑资产页面
function assetsEditPage(id){
	flushHtmlByAjax("/assets/editPage/"+id,"centerContent");
}

//编辑服务器页面
function serverEditPage(assetsId){
   flushHtmlByAjax("/assets/server/editPage/"+assetsId,"centerContent");
}

//kubernetes
function kubernetesConfigPage(){
	 flushHtmlByAjax("/k8s/configPage","centerContent");
}

function k8sInstall(id){
	 flushHtmlByAjax("/k8s/install/"+id,"centerContent");
}