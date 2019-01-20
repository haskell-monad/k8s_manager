BEGIN;
INSERT INTO "assets" VALUES (1, '', 2, 2, NULL, '2019-01-19', '2019-01-19', 'admin', '', '233hh', 22, '0301112122411', '高配 18年 大内存');
INSERT INTO "assets" VALUES (2, '', 3, 1, NULL, '2019-01-19', '2019-01-19', 'admin', '', 'D30', 20102, '009-123121', '双十一');
INSERT INTO "assets" VALUES (3, '', 5, 3, NULL, '2019-01-19', '2019-01-19', 'admin', '', 'F30', 23, 'G-0332', '思科产品');
COMMIT;

BEGIN;
INSERT INTO "install_check" VALUES (1, '验证版本', '/etc/ansible/bin/kubectl version', 'k8s', '描述信息啊', 'yes');
INSERT INTO "install_check" VALUES (2, '验证master/etcd', '/etc/ansible/bin/kubectl get componentstatus', 'k8s', '可以看到scheduler/controller-manager/etcd等组件 Healthy', 'yes');
INSERT INTO "install_check" VALUES (3, '验证apiserver', '/etc/ansible/bin/kubectl cluster-info', 'k8s', '可以看到kubernetes master(apiserver)组件 running', 'yes');
INSERT INTO "install_check" VALUES (4, '验证node', '/etc/ansible/bin/kubectl get node', 'k8s', '可以看到单 node Ready状态', 'yes');
INSERT INTO "install_check" VALUES (5, '集群pod状态', '/etc/ansible/bin/kubectl get pod --all-namespaces', 'k8s', '可以查看所有集群pod状态，默认已安装网络插件、coredns、metrics-server等', 'yes');
INSERT INTO "install_check" VALUES (6, '集群服务状态', '/etc/ansible/bin/kubectl get svc --all-namespaces', 'k8s', '可以查看所有集群服务状态', 'yes');
INSERT INTO "install_check" VALUES (7, '验证etcd', 'systemctl status etcd', 'etcd', '查看etcd服务状态', 'yes');
INSERT INTO "install_check" VALUES (8, 'etcd日志', 'journalctl -u etcd', 'etcd', '查看etcd运行日志', 'yes');
INSERT INTO "install_check" VALUES (9, '验证etcd集群', 'for ip in ${ETCD_CLUSTER}; do
  ETCDCTL_API=3 /etc/ansible/bin/etcdctl \
  --endpoints=https://${ip}:2379  \
  --cacert=/etc/kubernetes/ssl/ca.pem \
  --cert=/etc/etcd/ssl/etcd.pem \
  --key=/etc/etcd/ssl/etcd-key.pem \
  endpoint health; done', 'etcd', '三台 etcd 的输出均为 healthy 时表示集群服务正常。', 'no');
INSERT INTO "install_check" VALUES (10, '验证kube-apiserver', 'systemctl status kube-apiserver', 'k8s', '查看进程状态，安装master节点后，可查看', 'yes');
INSERT INTO "install_check" VALUES (11, '验证controller', 'systemctl status kube-controller-manager', 'k8s', '查看进程状态，安装master节点后，可查看', 'yes');
INSERT INTO "install_check" VALUES (12, '验证scheduler', 'systemctl status kube-scheduler', 'k8s', '查看进程状态，安装master节点后，可查看', 'yes');
INSERT INTO "install_check" VALUES (13, '查看apiserver日志', 'journalctl -u kube-apiserver', 'k8s', '查看进程运行日志', 'yes');
INSERT INTO "install_check" VALUES (14, '查看controller日志', 'journalctl -u kube-controller-manager', 'k8s', '查看进程运行日志', 'yes');
INSERT INTO "install_check" VALUES (15, '查看scheduler日志', 'journalctl -u kube-scheduler', 'k8s', '查看进程运行日志', 'yes');
INSERT INTO "install_check" VALUES (16, '查看组件状态', '/etc/ansible/bin/kubectl get componentstatus', 'k8s', '验证k8s-master的安装，可以看到scheduler/controller-manager等', 'yes');
INSERT INTO "install_check" VALUES (17, '查看haproxy进程', 'systemctl status haproxy', 'haproxy', '检查haproxy进程状态', 'yes');
INSERT INTO "install_check" VALUES (18, '查看haproxy日志', 'journalctl -u haproxy', 'haproxy', '检查进程日志是否有报错信息', 'yes');
INSERT INTO "install_check" VALUES (19, '查看keepalived进程', 'systemctl status keepalived', 'keepalived', '检查进程状态', 'yes');
INSERT INTO "install_check" VALUES (20, '查看keepalived日志', 'journalctl -u keepalived', 'keepalived', '检查进程日志是否有报错信息', 'yes');
INSERT INTO "install_check" VALUES (21, '查看端口监听', 'netstat -antlp|grep 8443', 'keepalived', '检查tcp端口是否监听，lb 节点验证', 'yes');
INSERT INTO "install_check" VALUES (22, 'keepalived主节点', 'ip a', 'keepalived', '检查 master的 VIP地址是否存在', 'no');
INSERT INTO "install_check" VALUES (23, '查看docker进程', 'systemctl status docker', 'docker', '服务状态', 'yes');
INSERT INTO "install_check" VALUES (24, '查看docker日志', 'journalctl -u docker', 'docker', '查看日志', 'yes');
INSERT INTO "install_check" VALUES (25, '查看 iptables', 'iptables-save|grep FORWARD', 'docker', '查看 iptables filter表 FORWARD链，最后要有一个 -A FORWARD -j ACCEPT 保底允许规则', 'yes');
INSERT INTO "install_check" VALUES (26, '查看kubelet进程', 'systemctl status kubelet', 'k8s-node', '查看进程状态', 'yes');
INSERT INTO "install_check" VALUES (27, '查看kube-proxy进程', 'systemctl status kube-proxy', 'k8s-node', 'kube-proxy', 'yes');
INSERT INTO "install_check" VALUES (28, '查看kubelet日志', 'journalctl -u kubelet', 'k8s-node', 'kubelet日志', 'yes');
INSERT INTO "install_check" VALUES (29, '查看kube-proxy日志', 'journalctl -u kube-proxy', 'k8s-node', 'kube-proxy日志', 'yes');
INSERT INTO "install_check" VALUES (30, '查看k8s-node状态', '/etc/ansible/bin/kubectl get node', 'k8s-node', '查看运行状态', 'yes');
INSERT INTO "install_check" VALUES (31, '查看dashboard', '/etc/ansible/bin/kubectl get pod -n kube-system | grep dashboard', 'dashboard', '验证dashboard', 'yes');
INSERT INTO "install_check" VALUES (32, '查看dashboard service', '/etc/ansible/bin/kubectl get svc -n kube-system|grep dashboard', 'dashboard', '查看dashboard service', 'yes');
INSERT INTO "install_check" VALUES (33, '查看集群服务dashboard', '/etc/ansible/bin/kubectl cluster-info|grep dashboard', 'dashboard', '查看集群服务', 'yes');
INSERT INTO "install_check" VALUES (34, '查看dashboard日志', 'kubectl logs kubernetes-dashboard-${log} -n kube-system', 'dashboard', '查看pod 运行日志', 'no');
INSERT INTO "install_check" VALUES (35, '令牌登陆dashboard-01', '/etc/ansible/bin/kubectl apply -f /etc/ansible/manifests/dashboard/admin-user-sa-rbac.yaml', 'dashboard', 'https://NodeIP:NodePort
令牌登录01(admin):  创建Service Account 和 ClusterRoleBinding', 'yes');
INSERT INTO "install_check" VALUES (36, '令牌登陆dashboard-02', '/etc/ansible/bin/kubectl -n kube-system describe secret $(/etc/ansible/bin/kubectl -n kube-system get secret | grep admin-user | awk ''{print $1}'')', 'dashboard', 'https://NodeIP:NodePort
令牌登录02(admin): 
获取 Bearer Token，找到输出中 ‘token:’ 开头那一行', 'yes');
INSERT INTO "install_check" VALUES (37, '令牌登陆dashboard_01', '/etc/ansible/bin/kubectl apply -f /etc/ansible/manifests/dashboard/read-user-sa-rbac.yaml', 'dashboard', '令牌登录（只读）
创建Service Account 和 ClusterRoleBinding', 'yes');
INSERT INTO "install_check" VALUES (38, '令牌登陆dashboard_02', '/etc/ansible/bin/kubectl -n kube-system describe secret $(/etc/ansible/bin/kubectl -n kube-system get secret | grep read-user | awk ''{print $1}'')', 'dashboard', '令牌登录（只读）
获取 Bearer Token，找到输出中 ‘token:’ 开头那一行', 'yes');
INSERT INTO "install_check" VALUES (39, '验证metrics-server', '/etc/ansible/bin/kubectl get apiservice|grep metrics', 'metrics-server', '查看生成的新api：v1beta1.metrics.k8s.io', 'yes');
INSERT INTO "install_check" VALUES (40, '查看kubectl-top命令', '/etc/ansible/bin/kubectl top node', 'metrics-server', '无需额外安装heapster', 'yes');
INSERT INTO "install_check" VALUES (41, '查看k8s-node网络', '/etc/ansible/bin/kubectl get pod -n kube-system', 'k8s-node', '验证新节点的网络插件calico 或flannel 的Pod 状态', 'yes');
INSERT INTO "install_check" VALUES (42, '验证Helm安装', '/etc/ansible/bin/kubectl get pod --all-namespaces|grep tiller', 'helm', '验证Helm安装', 'yes');
INSERT INTO "install_check" VALUES (43, '查看helm版本', 'helm version', 'helm', '查看版本', 'yes');
COMMIT;

BEGIN;
INSERT INTO "install_step" VALUES (-4, 'ansible环境准备', 'k8s_prepare_install_env', 1, -100, 'no', 1, '安装ansible环境，生成hosts文件等', NULL, '');
INSERT INTO "install_step" VALUES (-3, '免密钥登陆配置', 'k8s_config_ssh_login', 1, -4, 'no', 2, '免密钥登陆各个集群节点', NULL, '_ssh.yml');
INSERT INTO "install_step" VALUES (-2, '自定义操作', 'k8s_install_custom', 1, -3, 'yes', 3, '执行一些自定义操作，如配置速度快一些等dns等', NULL, '_custom.yml');
INSERT INTO "install_step" VALUES (-1, '导入k8s二进制/镜像文件', 'k8s_import_install_package', 1, -2, 'no', 4, '导入k8s二进制文件和docker镜像', NULL, '');
INSERT INTO "install_step" VALUES (0, '一键安装', 'xxxx', 3, NULL, 'yes', 1, '一键部署集群', NULL, '');
INSERT INTO "install_step" VALUES (1, '安装准备', 'k8s_init_depend', 2, -1, 'no', 1, '安装准备，安装一些必要的依赖', NULL, '01.prepare.yml');
INSERT INTO "install_step" VALUES (2, '安装k8s-etcd', 'k8s_instll_etcd', 2, 1, 'no', 2, '安装etcd集群等', NULL, '02.etcd.yml');
INSERT INTO "install_step" VALUES (3, '安装k8s-docker', 'k8s_install_docker', 2, 2, 'no', 3, '安装docker', NULL, '03.docker.yml');
INSERT INTO "install_step" VALUES (4, '安装k8s-master', 'k8s_install_master', 2, 3, 'no', 4, '安装master', NULL, '04.kube-master.yml');
INSERT INTO "install_step" VALUES (5, '安装k8s-node', 'k8s_install_node', 2, 4, 'no', 5, '安装node节点', NULL, '05.kube-node.yml');
INSERT INTO "install_step" VALUES (6, '安装k8s-network', 'k8s_install_network', 2, 5, 'no', 6, '安装网络插件', NULL, '06.network.yml');
INSERT INTO "install_step" VALUES (7, '安装k8s-plugins', 'k8s_install_plugins', 2, 6, 'no', 7, '安装一些必要的插件', NULL, '07.cluster-addon.yml');
INSERT INTO "install_step" VALUES (11, '安装Harbor', 'k8s_install_harbor', 6, 7, 'yes', 1, '安装harbor', NULL, '11.harbor.yml');
INSERT INTO "install_step" VALUES (12, '安全安装 helm（在线）', 'k8s_install_helm_online', 6, 7, 'yes', 2, '安装helm', NULL, '');
INSERT INTO "install_step" VALUES (13, '安全安装 helm（离线）', 'k8s_install_helm_offline', 6, 7, 'yes', 3, '安装helm', NULL, '');
INSERT INTO "install_step" VALUES (14, '安装Jenkins', 'k8s_install_jenkins', 6, 7, 'yes', 4, '安装jenkins', NULL, '');
INSERT INTO "install_step" VALUES (15, '安装Gitlab', 'k8s_install_gitlab', 6, 7, 'yes', 6, '安装gitlab', NULL, '');
INSERT INTO "install_step" VALUES (20, '新增k8s-node节点', 'k8s_install_new_node', 4, 7, 'yes', 1, '增加node节点', NULL, '20.addnode.yml');
INSERT INTO "install_step" VALUES (21, '新增k8s-master节点', 'k8s_install_new_master', 4, 7, 'yes', 2, '新增master节点', NULL, '21.addmaster.yml');
INSERT INTO "install_step" VALUES (22, '删除集群节点', 'k8s_install_remove_node', 5, 7, 'yes', 1, '移除k8s集群中的节点', 'clean_one_node_1.yml', 'tools/clean_one_node.yml');
INSERT INTO "install_step" VALUES (99, '清理集群', 'k8s_install_clear', 3, NULL, 'yes', 2, '一键清理集群', NULL, '99.clean.yml');
COMMIT;


BEGIN;
INSERT INTO "kube_cluster" VALUES (1, 1, '192.168.150.184', 'test.harbor.com', 'harbor', 'root', 'Linux2019', 22, NULL, 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (2, 1, '192.168.150.181', NULL, 'k8s', 'root', 'Linux2019', 22, NULL, 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (3, 1, '192.168.150.182', NULL, 'k8s', 'root', 'Linux2019', 22, NULL, 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (4, 1, '192.168.150.184', NULL, 'k8s', 'root', 'Linux2019', 22, NULL, 'backup', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (5, 1, '192.168.150.181', NULL, 'etcd', 'root', 'Linux2019', 22, 'etcd1', 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (6, 1, '192.168.150.182', NULL, 'etcd', 'root', 'Linux2019', 22, 'etcd2', 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (7, 1, '192.168.150.183', NULL, 'etcd', 'root', 'Linux2019', 22, 'etcd3', 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (8, 1, '192.168.150.185', NULL, 'loadbalance', 'root', 'Linux2019', 22, NULL, 'master', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
INSERT INTO "kube_cluster" VALUES (9, 1, '192.168.150.186', NULL, 'loadbalance', 'root', 'Linux2019', 22, NULL, 'backup', NULL, 'yes', '2019-01-19', '2019-01-19', 1);
COMMIT;

BEGIN;
INSERT INTO "kube_config" VALUES (1, 'test', 'v1.10', 'multi-master', '192.168.150.181', 'yes', 'yes', '20000-40000', '192.168.150.187', 'https://192.168.150.187:8443', 'flannel', '10.68.0.0/16', '172.20.0.0/16', '10.68.0.1', '10.68.0.2', 'cluster.local.', 'admin', 'admin123456', '/opt/kube/bin', '/etc/kubernetes/ssl', '/etc/ansible', 'no', '', -100, '集群描述啊', '2019-01-19', 'admin', '2019-01-19', '');
COMMIT;

BEGIN;
INSERT INTO "product" VALUES (1, '支付系统', '支付系统啊', '需求收集', '张三丰', 1000, '张无忌', 2000, '张起灵', 3000, '张副官', 4000, '', 'http://wiki.com/pay/index', '2019-01-19', '2019-01-19', 'admin', '', NULL, '');
INSERT INTO "product" VALUES (2, '移动端APP', '移动端app', '需求收集', '凌云', 333, '壮志', '020-2000', '岭南', '300-11121', '黑帽子', '040-2121', '', 'http://wiki.com/app/index', '2019-01-19', '2019-01-19', 'admin', '', NULL, '');
COMMIT;

BEGIN;
INSERT INTO "product_version" VALUES (1, 2, 'app-v1.0.0', '张学友', '2019-01-01', '2019-02-20', 'http://wiki.com/app/v1.0.0/index.html', 5, NULL, 333, '张无忌', '020-2000', '郭富城', 3000, '刘德华', '040-4000', '2019-01-19', '2019-01-19', 'admin', '', '商品 搜索 支付');
INSERT INTO "product_version" VALUES (2, 2, 'app-v2.0.0', '凌云', '2019-01-20', '2019-03-05', 'http://wiki.com/app/v2.0.0/index.html', 2, NULL, 333, '黎明', '020-2000', '张起灵', 3000, '刘德华', '040-4000', '2019-01-19', '2019-01-19', 'admin', '', '邀请 活动 周年庆');
COMMIT;





