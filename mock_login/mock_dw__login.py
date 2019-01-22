#-*- coding:utf-8 -*
from predict import *

import execjs
import requests
import json

def mock_login(cookie,verifyCode,verify_url,pubilicKey,login_url,dfdl_url):
    # code_url:  https://95598.gz.csg.cn/ai.do?an=rnd_4520750094   dfdl_url:  https://95598.gz.csg.cn/df/dldffx.do
    #  账号：15121601911,密码：sn123456789
    #  账号 nctext/jmdlm
    # 密码  mmtxt/ jmmm
    # 验证码  verifyCode2
    # 密码加密
    #  var publicKey = '87cbc10c-2e96-4c4a-96ff-b78ee974552f_c72cb115bbf6b39c0ba69d7dd2c21dca292f19cdfea8f13270a780b0f31ff3316f0a5a5695a2644db785c6e3374198914bcc6b26f8cec6ba643cdcb1824c48c1';
    #$("#mmtext").val(doRSAEncrypt(publicKey, pwd));
    #$("#nctext").val(doRSAEncrypt(publicKey, zh));
    verify_r = checkVerifyCode(cookie,verifyCode, verify_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': cookie
        }
    zh = ctx.call("doRSAEncrypt",
                  pubilicKey,
                  "15121601911")
    mm = ctx.call("doRSAEncrypt",
                  pubilicKey,
                  "sn123456789")

    #mm="66d26724-e747-4d85-bbf2-4430205bfa62_099f5cf80ac115746cd5bc6e19e003fa4b66568cc942bd63267286746469b53b7255534ec0dcb909184fb9cac8bd44c70eb4ea51c2dc7beeb76be7347a177708"
    #  66d26724-e747-4d85-bbf2-4430205bfa62_099f5cf80ac115746cd5bc6e19e003fa4b66568cc942bd63267286746469b53b7255534ec0dcb909184fb9cac8bd44c70eb4ea51c2dc7beeb76be7347a177708
    #zh="66d26724-e747-4d85-bbf2-4430205bfa62_23d490c095f77b387646ddbb923acbb41212d20d9cb963f63d8ca100c03fb162e86ca3f881036aba3eb306f347001910d8832985ef65eaf30cf3e24796feb9b5"
    #  66d26724-e747-4d85-bbf2-4430205bfa62_23d490c095f77b387646ddbb923acbb41212d20d9cb963f63d8ca100c03fb162e86ca3f881036aba3eb306f347001910d8832985ef65eaf30cf3e24796feb9b5
    # action=yhdl&checkOnline=true&rurl=&dlxx.zhlx=2&dlxx.dllx=1&wxSwitch=ON&dlmjy=&mmjy=&tempFlag1=N&zcdl=&jmdlm=3280db68-c651-440c-b7a9-b49c4acb6107_19e70de06e3c4072c207ef4b46c5838f034aca3776c91f4e33a1e7ee4fa90b65d1e3288804bb6f664fad062e874dffe4a04587462c6596ee1258020faa55bec9&jmmm=3280db68-c651-440c-b7a9-b49c4acb6107_a4883687d394d25d7e848209182e34f6a2e36e675cb42e13c2ac01e5fadf21a0de63273c536c863e29ef706abc9fced82c50cb0a4f62623d9de158172e178e27&verifyCode2=aqhz&dlxx.sjh=&dlxx.sjyzm=&verifyCode=
    login_data={
        "jmdlm":zh,
         "jmmm":mm,
        "verifyCode2":verifyCode,
        "action":"yhdl",
        "checkOnline":"true",
        "wxSwitch":"ON",
        "tempFlag1":"N",
        "dlxx.dllx": "1",
        "dlxx.zhlx":"2",
        "rurl":"",
        "dlmjy":"",
        "mmjy":"",
        "zcdl":"YES",
        "dlxx.sjh":"",
        "dlxx.sjyzm":"",
        "verifyCode":""
    }
    print("login_data=%s" % json.dumps(login_data))
   # s = requests.Session()
    login_r = requests.post(login_url, headers=headers, data=login_data,verify=False)
    print("cookies=%s"%login_r.headers)
    # res.cookies["cookie_name"]
    dfcz_data={
        "ksny":"201801",
        "jzny":"201812",
        "glyhbh":"0622089504031565",
    }

    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': login_r.headers['Set-Cookie']
        }
    print("headers1=%s"%headers1['Cookie'])
    dfdl_r = requests.post(dfdl_url, headers=headers1, data=dfcz_data,verify=False)
    print("dfdl_r=%s"%dfdl_r.text)



def get_js(path):
    f = open(path, 'r')  # 打开JS文件
    line = f.readline()
    html_str = ''
    while line:
        html_str = html_str + line
        line = f.readline()
    return html_str


def load_js(js_str):
    return execjs.compile(js_str)


# cvc.do
def checkVerifyCode(cookie,code,url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': cookie
        }

    verify_data={
        "vc":code,
        "action":"checkVerifyCode",
    }
    page_r=requests.post(url,data=verify_data,headers=headers,verify=False)
    print("code_page-r=%s"%page_r.text)
    return page_r




if __name__ == '__main__':
    rsa_js_path="../js/rsa.js"
    ctx = load_js(get_js(rsa_js_path))
    #zh=ctx.call("doRSAEncrypt", "66d26724-e747-4d85-bbf2-4430205bfa62_a1ef538486e142d7d6da0ec5a2edc1be0fba72fb38d567626d32e279cc8a70bf08c12f17e0f02810a705c54a210cbe33299d9d085faab3616568a3536a5052b5", "15121601911")
    #mm=ctx.call("doRSAEncrypt", "66d26724-e747-4d85-bbf2-4430205bfa62_a1ef538486e142d7d6da0ec5a2edc1be0fba72fb38d567626d32e279cc8a70bf08c12f17e0f02810a705c54a210cbe33299d9d085faab3616568a3536a5052b5", "sn123456789")

    #print("zh=%s"%zh)
    #print("mm=%s" % mm)

    #checkVerifyCode("8qvv","https://95598.gz.csg.cn/cvc.do")
    #  账号：15121601911,密码：sn123456789
    # https://95598.gz.csg.cn/kh/khdlzy.do
    mock_login("WSYYTSESSION=H6dzb7Ca0Xhr-b2kWDnyMaPnP-tEc8LLsuQiWe3Pcj9t8gOLZemI!-940498615",
               "hehw",
               "https://95598.gz.csg.cn/cvc.do",
              "37a51c03-31f4-4d85-88aa-b4964b028fc5_9d4b4faa51697d9cc3a17c86580eaa19a31e8af172d3c3df1b18ded36713cf0da27ceb7a6ce21ea4cc7121df96366770e461b0cd23a51ad60c7365d365bff6d3",
               "https://95598.gz.csg.cn/yhdl.do",
               "https://95598.gz.csg.cn/df/dldffx.do")

