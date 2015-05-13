## ZabbixAPI是Zabbix的python实现版本
#一、ZabbixAPI的用法
```
python>import ZabbixAPI
python>zbx=ZabbixAPI.ZabbixAPI()
#提供三个方法
zbx.login()           
zbx.logout()
zbx.APIobjectMethod() 

#zbx.APIobjectMethod(method='host.get', params={'output': 'extend'})
```
如history.get的官方例子用法如下,链接见https://www.zabbix.com/documentation/2.2/manual/api/reference/history/get
```
{
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 0,
        "itemids": "23296",
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 10
    },
    "auth": "038e1d7b1735c6a5436ee9eae095879e",
    "id": 1
}
```
则
```
zbx.APIobjectMethod(method='host.get',"params": {
        "output": "extend",
        "history": 0,
        "itemids": "23296",
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 10
    }
}
```
为其调用方法

#二、tools.py是一个基于ZabbixAPI的例子
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
