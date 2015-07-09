## ZabbixAPI是Zabbix的python实现版本
#一、ZabbixAPI的用法
```
shell#git clone https://github.com/itnihao/ZabbixAPI.git
shell#cd ZabbixAPI
#安装
shell#sudo python setup.py install
```

#配置用户名、密码：
```
#修改/etc/.zbx_tool.cfg如下
 #cat /etc/.zbx_tool.cfg
 [auth]
 URL=http://zabbix.itnihao.com
 Username=User
 Password=Pass
 [http_auth]
 HttpUsername=HttpUser
 HttpPassword=HttpPass
 
 #cat /etc/.zbx_tool.cfg
 [auth]
 URL=http://zabbix.itnihao.com
 Username=User                                                                                                                   Password=Pass
 [http_auth]
 HttpUsername=''
 HttpPassword=''
```

#使用API
```
python>from ZabbixAPI import  ZabbixAPI
python>zabbix = ZabbixAPI("https://zabbix.itnihao.com")
如果需要执行HTTP Basic认证，请执行auth方法
python>zabbix.session.auth=(HttpUsername,HttpPassword)
python>zabbix.login(Username,Password)
#提供三个方法
zbx.login()           
zbx.logout()
zbx.APIobjectMethod() 
host=zbx.APIobjectMethod(method='host.get', params={'output': 'extend'})
for h in host:
    print h['host']
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
则history.get的调用方法如下:
```
zbx.APIobjectMethod(method='history.get',"params": {
        "output": "extend",
        "history": 0,
        "itemids": "23296",
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 10
    }
}
```

#二、zbx_tool是一个基于ZabbixAPI的例子
##1.功能:
```
    1.查询主机 主机组 模板 
    2.添加主机 主机组 
    3.查询主机的特定items数据
    4.查询主机组的特定items数据
```

##2.用法
 zbx_tool --help查看帮助 
 

