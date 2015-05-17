#!/usr/bin/env python
#coding=utf-8
#author: itnihao
#date:   2015-05-13

import sys
import json
import requests


class ZabbixAPI:
    """docstring for ZabbixAPI"""
    def __init__(self):
        self.zabbix_url = "http://localhost/api_jsonrpc.php"
        #self.zabbix_url = "http://localhost/zabbix/api_jsonrpc.php"
        self.zabbix_header = {
                              "Content-Type" : "application/json", 
                              "User-Agent"   : "python/ZabbixAPI" 
        }
        self.zabbix_user   = "Admin" 
        self.zabbix_pass   = "zabbix"
#        self.auth_code     = ""

    def login(self):
        params = json.dumps(
                {
                    "jsonrpc":"2.0",
                    "method":"user.login",
                    "params":
                            {
                                "user": self.zabbix_user,
                                "password": self.zabbix_pass,
                            },
                    "id":0
        })

        #判断是否登录
        try:
            self.check_auth
        except:
            self.check_auth=0

        #如果未登录，执行login
        if self.check_auth == 0:
            try:
                request_zabbix = requests.post(self.zabbix_url, data=params, headers=self.zabbix_header,timeout=5)
            except Exception as e:
                print e
            else:
                response=request_zabbix.json()
                request_zabbix.close()
                if  'result'  in  response:
                    self.auth_code=response['result']
                    ret=self.auth_code
                    self.check_auth=1
                else:
                    self.auth_code=response['error']['data']
                    ret=self.auth_code
        #已登录的不再执行登录
        else:
            ret=self.auth_code
        return ret

    def  logout(self):
        '''
         退出登录
        '''
        if self.login() is not None:
            auth_data = json.dumps({
                "jsonrpc": "2.0",
                "method": "user.logout",
                "params": [],
                "id": 1,
                "auth": self.login()
            })
        try:
            request_zabbix = requests.post(self.zabbix_url, data=auth_data, headers=self.zabbix_header,timeout=5)
        except Exception as e:
            print e
        else:
            response = request_zabbix.json()
            request_zabbix.close()
            if not response['result']:
                print "logout failed"

    def APIobjectMethod(self,method='host.get',params={"output":"extend"}):
        json_data={
                "method" : method, 
                "params" : params
        }
        json_base={
                "jsonrpc":"2.0",
                "auth": self.login(),
                "id":1
        }
        json_data.update(json_base)
        if len(self.login()) == 0:
            print 'Not login'
            sys.exit(1)
        if len(self.login()) != 0:
            params = json.dumps(json_data) 
            request_zabbix = requests.post(self.zabbix_url, data=params, headers=self.zabbix_header,timeout=20)
            request_zabbix.close()
            response = request_zabbix.json()

            if 'result' in response:
                ret=response['result']
                if len(ret) != 0:
                    return ret
                elif len(ret) == 0:
                    return 'error'
            elif 'error' in response:
                print response['error']
