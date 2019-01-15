# -*- coding: UTF-8 -*-
from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
import json
from mock_login import *
import  requests

# 我们自定义一个类试试
class User(object):
    def __init__(self, loginName,loginSecret):
        self.loginName = loginName
        self.loginSecret=loginSecret


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.loginName,obj.loginSecret
        return json.JSONEncoder.default(self, obj)



def mock_login(login_url):
    #登陆地址
    #login_url = 'http://www.jobbole.com/wp-admin/admin-ajax.php'
    #User-Agent信息
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    #Headers信息
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive','Content-Type':'application/json'}
    #登陆Form_Data信息
    loginUser={
        "loginName":"vimi8",
        "loginSecret":"123"
    }#loginUser(loginName='vimi8', loginSecret='123')

    queryParam = {
        "index":"1",
        "size":"3",
    }
    json_2 = {'loginUser': User('vimi8', '123')}

    #创建Request对象

    response = requests.post(login_url, data=json.dumps(loginUser), headers=head)
    print('response=%s' % response.headers['SET-COOKIE'])
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive', 'Content-Type': 'application/json','Cookie':response.headers['SET-COOKIE']}
    #req1 = request.Request(url='http://bigdata.vimi8.top/api/industrial_db/around_scenery', headers=head)
    try:
        #使用自己创建的opener的open方法
       # response1 = opener.open(req1)
      #  html = response1.read().decode('utf-8')
      #  print('reponse1=%s'%  html)
        response2 = requests.get(url='http://industrial_db.vimi8.top/api/industrial_db/around_scenery?index=1&size=2',data=json.dumps(queryParam), headers=head)
        print("reponse2=%s" % response2.text)
    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError:%d" % e.code)
        elif hasattr(e, 'reason'):
            print("URLError:%s" % e.reason)

if __name__ == '__main__':
    mock_login('http://bigdata.vimi8.top/auth/login/')
    #json_2 = {'user': User('orangle','123')}

    #print('json-dumps=%s'%json.dumps(json_2, cls=UserEncoder))