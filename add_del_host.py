#!/usr/bin/python
# -*- coding:utf-8 -*-
#注意组的 id  可以写成一个变量
import urllib,requests,json
from urllib import urlencode

server_url = "http://falcon.sprucetec.com"         ##服务的域名或IP:1234
r = requests.get(server_url+"/sso/sig")            ##获取cookie的接口
sig_id = r.content

def cookie_falcon():                    ##进行单点登录（Portal 只有这个模块下的接口会有这个验证）
    data = { "name": "username",
    "password": "xxxxx",
    "ldap": 1,
    "sig": sig_id,
    "callback": "docker"            ##这个好像可以随便写
    }
    postData = urllib.urlencode(data)
    req = urllib.urlopen(server_url+"/auth/login",postData)
    content = req.read()
    print content
if __name__ == '__main__':
    cookie_falcon()

def add_docker_falcon(ipid):
    urlvalue = {"group_id":9}
    urlvalue["hosts"] = ipid
    values = urlencode(urlvalue)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
              }
    quest = requests.post('http://portal.falcon.sprucetec.com/host/add',data=values,headers=headers,cookies={"sig":sig_id})
    print quest.content
#if __name__ == '__main__':
#    add_docker_falcon("haha")

def del_docker_falcon(conid):
    id = requests.get('http://portal.falcon.sprucetec.com/host/' + conid + "/get_id", cookies={"sig": sig_id})   ##这个接口内部写的
#    print id.content
    urlvalue = {"grp_id": 9}
    urlvalue["host_ids"] = json.loads(id.content)['msg'][0]
    print urlvalue["host_ids"]
    values = urlencode(urlvalue)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    quest = requests.post('http://portal.falcon.sprucetec.com/host/remove',data=values,headers=headers,cookies={"sig":sig_id})
    print quest.content
#if __name__ == '__main__':
#    del_docker_falcon("haha")
