jQuery(document).ready(function(){

		jQuery("#_product").validate({
			rules: {
				productName: "required",
				productWiki: "required",
				
				productManager: "required",
				productContact: "required",
				
				devManager: "required",
				devContact: "required",
				
				qaManager: "required",
				qaContact: "required",

				safeManager: "required",
				safeContact: "required",

				productDesc: "required",
				
				// email: {
				// 	required: true,
				// 	email: true,
				// },
			},
			messages: {
				productName: "请输入产品名称",
				productWiki: "请输入产品Wiki地址",
				productManager: "请输入产品负责人姓名",
				productContact: "请输入产品负责人联系方式",

				devManager: "请输入开发负责人姓名",
				devContact: "请输入开发负责人联系方式",

				qaManager: "请输入测试负责人姓名",
				qaContact: "请输入测试负责人联系方式",

				safeManager: "请输入安全测试负责人姓名",
				safeContact: "请输入安全测试负责人联系方式",

				productDesc: "请输入产品线简单描述信息"
			}
		});


		jQuery("#_version").validate({
			rules: {
				versionName: "required",
				versionStatus: "required",
				startTime: "required",
				endTime: "required",
				// versionEnv: "required",	
				versionWiki: "required",
				
				productManager: "required",
				productContact: "required",
				
				devManager: "required",
				devContact: "required",
				
				qaManager: "required",
				qaContact: "required",

				safeManager: "required",
				safeContact: "required",
				tags: "required",	
				productId: "required",
			},
			messages: {
				versionName: "请输入版本名称",
				versionStatus: "请选择当前版本状态",
				startTime: "请选择版本开始日期",
				endTime: "请选择版本截止日期",
				// versionEnv: "请选择版本当前环境",
				versionWiki: "请输入版本Wiki需求地址",
				
				productManager: "请输入产品负责人姓名",
				productContact: "请输入产品负责人联系方式",

				devManager: "请输入开发负责人姓名",
				devContact: "请输入开发负责人联系方式",

				qaManager: "请输入测试负责人姓名",
				qaContact: "请输入测试负责人联系方式",

				safeManager: "请输入安全测试负责人姓名",
				safeContact: "请输入安全测试负责人联系方式",
				tags: "请输入产品标签",		
				productId: "请选择产品"
			}
		});


		jQuery("#_assets").validate({
			rules: {
				assetType: "required",
				status: "required",
			},
			messages: {
				assetType: "请选择资产类型",
				status: "请选择设备状态",
			
			}
		});


		jQuery("#_server").validate({
			rules: {
				manageIp: "required",
				intranetIp: "required",
				user: "required",
				ip: "required",
				port: "required",		
				desc: "required",
				id: "id",
			},
			messages: {
				manageIp: "请输入管理IP",
				intranetIp: "请输入内网IP",
				user: "请输入SSH用户名",
				ip: "请输入IP地址",
				port: "请输入SSH端口",
				desc: "请输入一些服务器描述信息",
				id: "资产id不可以为空",
			}
		});
});
