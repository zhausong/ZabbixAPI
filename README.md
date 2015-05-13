# ZabbixAPI
##1.功能:
```
    1.查询主机 主机组 模板 
    2.添加主机 主机组 
    3.查询主机的特定items数据
    4.查询主机组的特定items数据
```

##2.用法
 python tools.py查看帮助 
 
##3.配置用户名、密码：
    修改ZabbixAPI.py如下
```
self.zabbix_url    = "http://localhost/api_jsonrpc.php"
self.zabbix_user   = "Admin" 
self.zabbix_pass   = "zabbix"
```
