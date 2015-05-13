#coding=utf8 
#author: itnihao    
#date:   2015-05-13 

import ZabbixAPI
import sys
import time
try:
    import argparse
except:
    print 'argparse module not exist,you can run pip install argparse'


zabbix = ZabbixAPI.ZabbixAPI()
auth_code=zabbix.login()

def host_get(hostname=''): 
    host=zabbix.APIobjectMethod(method='host.get',params={"output":"extend","filter":{"host":hostname}})
    status = {"0":"OK","1":"Disabled"}
    available = {"0":"Unknown","1":"available","2":"Unavailable"}
    if host != 'error':
        host=host[0]
        print "HostName: %s\t HostID: %s\t Status:\033[32m%s\033[0m \t Available:\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
    else:
        print "HostName: %s\t Status: %s\t" %(hostname,'not exist')

def hostgroup_get(hostgroupName=''):  
    group = zabbix.APIobjectMethod(method='hostgroup.get',params={"output": "extend", "filter": { "name": hostgroupName }})
    if type(group) is list:
        print "GroupName: %s\t GroupID: %s"% (group[0]['name'],group[0]['groupid'])
    else:
        print "GroupName: %s\t GroupID: %s"% (hostgroupName,'does not exist')

def template_get(template=''):
    template = zabbix.APIobjectMethod(method='template.get',params={"output":"extend","filter":{"name":template}})
    for i in template:
        print i['templateid'],i['host']
    return template

def host_create(hostName,hostIP,groupName,template):
    host = zabbix.APIobjectMethod(method='host.create',params={ 
                                     "host": hostName, 
                                     "interfaces": [ 
                                     { 
                                     "type": 1, 
                                     "main": 1, 
                                     "useip": 1,
                                     "ip": hostIP ,
                                     "dns": hostName,
                                     "port": "10050" 
                                      } 
                                     ], 
                                   "groups": groupName,
                                   "templates": template})
    print "添加主机 : \033[42m%s\031[0m \tid :\033[31m%s\033[0m" % (hostip, host['result']['hostids']) 


def hostgroup_create(hostgroupName=''):
    group=zabbix.APIobjectMethod(method='hostgroup.get',params={"output": "extend", "filter": { "name": hostgroupName }})
    if type(group) is list:
        if 'groupid' in group[0]:
            print "hostgroupName:\t %s exist,GroupID:\t %s"%(hostgroupName,group[0]['groupid']) 
    if group == 'error':
        ret=zabbix.APIobjectMethod(method="hostgroup.create",params={"name":hostgroupName}) #
        groupid=int(ret['groupids'][0])
        print "\033[042m 添加主机组:%s\033[0m  hostgroupID : %s"%(hostgroupName,groupid)

def host_delete(hostid):
    hostid_list=[]
        #print type(hostid)
    for i in hostid.split(','):
        var = {}
        var['hostid'] = self.host_get(i)
        hostid_list.append(var)		 
    data=zabbix.APIobjectMethod(method ='host.delete',params={hostid_list})
    #print "主机 \033[041m %s\033[0m  已经删除 !"%(hostid_list)
    #print "主机%s已经删除!"

def host_disable(hostip):
    host=zabbix.APIobjectMethod(method="host.update",params={"hostid": self.host_get(hostip),"status": 1})
    #print '----主机现在状态------------'
    print host_get(hostip)

def get_items_value(hostid='',item='',startime='',endtime=''):
    #时间转时间戳
    startime=int(time.mktime(time.strptime(startime,'%Y-%m-%d %H:%M:%S')))
    endtime=int(time.mktime(time.strptime(endtime,'%Y-%m-%d %H:%M:%S')))
    hostname=zabbix.APIobjectMethod(method='host.get',params={"output":["host"],"filter":{"hostid":hostid}})
    if 'host' not in hostname[0]:
        hostname='null'
    else:
        hostname=hostname[0]['host']
        hostname=str(hostname)
    items=zabbix.APIobjectMethod(method='item.get',params={"output":['itemid','value_type'],"hostids":hostid,"search":{"key_":item},"sortfileld":"name"})
    #itemid=items['itemid']
    if type(items) is list:
        items=items[0]
        if type(items) is dict:
            itemid=int(items['itemid'])
            item_type=int(items['value_type'])
    else:
        print "item is Error"
    #    return 'Error'
    history_value=zabbix.APIobjectMethod(method='history.get',params={"output": "extend","history": item_type,"itemids": itemid,"time_from":startime,"time_till":endtime,"sortfield": "clock","sortorder": "DESC"})
    if type(history_value) is not list:
        print 'Error'
        sys.exit(1)
    item_value=[]
    for value in history_value:
        v=float(value['value'])
        item_value.append(v)
    v_max=max(item_value)
    v_min=min(item_value)
    v_avg=sum(item_value)/len(item_value)
    v_count=len(item_value)
    #print "MAX: %s, MIN:%s,AVG:%s"%( v_max, v_min , v_avg )
    print {"HOSTNAME":hostname,"MAX":v_max,"MIN":v_min,"AVG":v_avg,"Count":v_count}
    return {"HOSTNAME":hostname,"MAX":v_max,"MIN":v_min,"AVG":v_avg,"Count":v_count}

def get_group_items_value(groupname='',item='',startime='',endtime=''):
    #host=zabbix.APIobjectMethod(method='hostgroup.get',params={"selectHosts": "extend", "filter": { "name": groupname}})
    host=zabbix.APIobjectMethod(method='hostgroup.get',params={"selectHosts": ['name','hostid'], "filter": { "name": groupname}})
    if type(host) is list:
    	if 'hosts' in host[0]:
            hosts=host[0]['hosts']
        else:
        	print "hosts not exist return exit"
        	sys.exit(1)
    else:
        print "Error and exit"
        sys.exit(1)
    #[{u'hostid': u'10255', u'name': u'd102-app-10'},
    # {u'hostid': u'10256', u'name': u'd102-app-11'},
    # {u'hostid': u'10261', u'name': u'd102-app-09'},
    # {u'hostid': u'10264', u'name': u'd102-app-07'},
    # {u'hostid': u'10296', u'name': u'd102-app-08'}]
    hostid_list=[]
    for k in hosts:
        hostid_list.append(int(k['hostid']))
    host_item_value_list=[]
    for hid in hostid_list:
        value=get_items_value(hostid=hid,item=item,startime=startime,endtime=endtime)
        host_item_value_list.append(value)
    max_list=[]
    min_list=[]
    avg_list=[]

    for k in host_item_value_list:
        max_list.append(float(k['MAX']))
    for k in host_item_value_list:
        min_list.append(float(k['MIN']))
    for k in host_item_value_list:
        avg_list.append(float(k['AVG']))
    MAX=sum(max_list)/len(max_list)
    MIN=sum(min_list)/len(min_list)
    AVG=sum(avg_list)/len(avg_list)

    #print "MAX:  %s\tMIN:   %s\tAVG:    %s"%(MAX,MIN,AVG)
    print {"HOSTGROUP":groupname,"ITEMNAME":item,"MAX":MAX,"MIN":MIN,"AVG":AVG}

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='zabbix  api ',usage='%(prog)s [options]')
    parser.add_argument('-H','--host',nargs='?',dest='listhost',default='host',help='查询主机')
    parser.add_argument('-G','--group',nargs='?',dest='listgroup',default='group',help='查询主机组')
    parser.add_argument('-T','--template',nargs='?',dest='listtemp',default='template',help='查询模板信息')
    parser.add_argument('-A','--add-group',nargs=1,dest='addgroup',help='添加主机组')
    parser.add_argument('-C','--add-host',dest='addhost',nargs=4,metavar=('10.10.10.1','HostName', 'test01,test02', 'Template01,Template02'),help='添加主机,多个主机组或模板使用分号')
    parser.add_argument('-d','--disable',dest='disablehost',nargs=1,metavar=('10.10.10.1'),help='禁用主机')
    parser.add_argument('-V','--getvalue',dest='getvalue',nargs=4,metavar=('10607','agent.ping','1431331816','1431331816'),help="获取历史数据")
    parser.add_argument('--get_group_items',dest='get_group_items',nargs=4,metavar=('groupname','itemsname','2015-05-12 00:00:01','2015-05-13 00:00:01'),help='查询主机组的items')
    parser.add_argument('-D','--delete',dest='deletehost',nargs='+',metavar=('10.10.10.1'),help='删除主机,多个主机之间用分号')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv)==1:
        print parser.print_help()
    else:
        args=parser.parse_args()
        if args.listhost != 'host' :
            if args.listhost:
                host_get(args.listhost)
            else:
                host_get()
        if args.listgroup !='group':
            if args.listgroup:
                hostgroup_get(args.listgroup)
            else:
                zabbix.hostgroup_get()
        if args.listtemp != 'template':
            if args.listtemp:
                template_get(args.listtemp)
            else:
                template_get()
        if args.addgroup:
            hostgroup_create(args.addgroup[0])
        if args.addhost:
            host_create(args.addhost[0],args.addhost[1], args.addhost[2], args.addhost[3])
        if args.disablehost:
            host_disable(args.disablehost)
        if args.deletehost:
            host_delete(args.deletehost[0])
        if args.getvalue:
            get_items_value(args.getvalue[0],args.getvalue[1],args.getvalue[2],args.getvalue[3])
        if args.get_group_items:
            get_group_items_value(args.get_group_items[0],args.get_group_items[1],args.get_group_items[2],args.get_group_items[3])
    zabbix.logout()

#python tools.py --getvalue        hostname  system.cpu.util[,iowait] '2015-05-11 18:12:01' '2015-05-12 18:12:01'
#python tools.py --get_group_items groupname system.cpu.util[,iowait] '2015-05-11 18:12:01' '2015-05-12 18:12:01'
