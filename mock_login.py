#-*- coding:utf-8 -*
from predict import *

import execjs
import requests
from urllib import request, parse
import ssl
from bs4 import BeautifulSoup

from requests.cookies import RequestsCookieJar

def crawlingDW(text,related_id):
    arr=[]
    soup = BeautifulSoup(text, 'html.parser')
    all_a = soup.find_all('table')
    if len(all_a)>0:
        dldf_a=all_a[0]
        print("dfdl-text=%s"%dldf_a)

        for tr in dldf_a.findAll('tr'):
            print('td0=%s'%tr.findAll('td')[0].getText())
            year=tr.findAll('td')[0].getText().strip().replace('\n','')
            if len(year)==6:
                value=(related_id,tr.findAll('td')[0].getText().strip().replace('\n',''),tr.findAll('td')[1].getText().strip().replace('\n',''),tr.findAll('td')[2].getText().strip().replace('\n',''),
                       tr.findAll('td')[3].getText().strip().replace('\n',''),tr.findAll('td')[4].getText().strip().replace('\n',''))
                print(value)
                arr.append(value)
    return arr



def mock_login(login_url,verifyCode,dfdl_url):
    # code_url:  https://95598.gz.csg.cn/ai.do?an=rnd_4520750094   dfdl_url:  https://95598.gz.csg.cn/df/dldffx.do
    #  账号：15121601911,密码：sn123456789
    #  账号 nctext/jmdlm
    # 密码  mmtxt/ jmmm
    # 验证码  verifyCode2
    # 密码加密
    #  var publicKey = '87cbc10c-2e96-4c4a-96ff-b78ee974552f_c72cb115bbf6b39c0ba69d7dd2c21dca292f19cdfea8f13270a780b0f31ff3316f0a5a5695a2644db785c6e3374198914bcc6b26f8cec6ba643cdcb1824c48c1';
    #$("#mmtext").val(doRSAEncrypt(publicKey, pwd));
    #$("#nctext").val(doRSAEncrypt(publicKey, zh));
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        #'Cookie': 'HttpOnly; WSYYTSESSION=jjLMBypJUpoILQMF4wOxDr08tR6wsx3Eq2i6rCmoNXKL1frXQ-FY!-519645265;'
        }
    zh = ctx.call("doRSAEncrypt",
                  "87cbc10c-2e96-4c4a-96ff-b78ee974552f_c72cb115bbf6b39c0ba69d7dd2c21dca292f19cdfea8f13270a780b0f31ff3316f0a5a5695a2644db785c6e3374198914bcc6b26f8cec6ba643cdcb1824c48c1",
                  "15121601911")
    mm = ctx.call("doRSAEncrypt",
                  "87cbc10c-2e96-4c4a-96ff-b78ee974552f_c72cb115bbf6b39c0ba69d7dd2c21dca292f19cdfea8f13270a780b0f31ff3316f0a5a5695a2644db785c6e3374198914bcc6b26f8cec6ba643cdcb1824c48c1",
                  "sn123456789")

    login_data={
        "jmdlm":zh,
         "jmmm":mm,
        "verifyCode2":verifyCode,
        "action":"yhdl",
        "checkOnline":"true",
        "wxSwitch":"ON",
        "tempFlag1":"N",

    }
   # s = requests.Session()
    login_r = requests.post(login_url, headers=headers, data=login_data)
    print("cookies=%s"%login_r.headers)
    print("login_r=%s" % login_r.text)
    # res.cookies["cookie_name"]
    dfcz_data={
        "ksny":"201801",
        "jzny":"201812",
        "glyhbh":"0622089504031565",
    }

    # Zi7KfnBdvYyXXkho8gb5_nT34jk3Kr8dRufop2lvUw11HALqtC9F!245646071
    cookies={"Hm_lvt_272a540ced697dcad590241ed2c39f62":"1543826537,1543830216,1544062172,1545272281",
             "Hm_lpvt_272a540ced697dcad590241ed2c39f62":"1545272281",
             "Hm_lvt_5ee2c8d53bcf6137d454d6bdeb6985a0":"1543826744,1543994006,1545272480",
             "Hm_lpvt_5ee2c8d53bcf6137d454d6bdeb6985a0":"1545292605",
             "WSYYTSESSION": "jzbKndU41SvI9HsASFJeonnY3RDxHk-Fshrl7x4veiXkREdTvmfu!-1857749737"}
    #dfdl_r = requests.post(dfdl_url, headers=headers, data=dfcz_data)
    #print("dfdl_r=%s"%dfdl_r.text)
    #print("cookies-dl=%s"%dfdl_r.cookies)


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

def exportExcel(url,glyhbh):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': 'HttpOnly; WSYYTSESSION=LZfU6Vx9zMxOKDHdmAKE0rYuJRy0F1j_fah3C4aYiu936JX4gZwJ!-1857749737;'
        }
    # 下载excel之前  先请求df/zdcx.do 保存参数值在服务端
    param_save={
        "action":"pageTo",
        "glyhbh":glyhbh,
        "ckqs":"12"
    }
    s = requests.Session()
    param_save_r = s.post("https://95598.gz.csg.cn/df/zdcx.do", data=param_save, headers=headers)
    print("param_save_r=%s"%param_save_r.text)
    # 下载excel

    data_param={
        #"ckqs":"12",
        "action":"exportExcel",
       # "glyhbh":glyhbh,
    }
    obtain_code_r = s.post(url, data=data_param,headers=headers)
    f = open(path+'/excel/'+glyhbh+'.xls', 'wb')
    # 将response的二进制内容写入到文件中
    f.write(obtain_code_r.content)
    # 关闭文件流对象
    f.close()

# cvc.do
def checkVerifyCode(code,url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': 'WSYYTSESSION=ohDQyk078SYvG5AymKHCBjKEoj7vm-lo0LZ1JxeyOWdc8kXmMZlV!1944680279;'
        }
    # 获取验证码
    # s = requests.Session()
    # obtain_code_r = s.get("https://95598.gd.csg.cn/ai.do?an=rnd_6564258381", headers=headers)
    # f = open('valcode.png', 'wb')
    # # 将response的二进制内容写入到文件中
    # f.write(obtain_code_r.content)
    # # 关闭文件流对象
    # f.close()

    #  print("cookies=%s" % obtain_code_r.headers)




    verify_data={
        "vc":code,
        "action":"checkVerifyCode",
    }
    # data = parse.urlencode(verify_data).encode('utf-8')
    # req = request.Request(url, headers=headers, data=data)
    # code_page = request.urlopen(req).read()
    # page_r = code_page.decode('utf-8')

    page_r=requests.post(url,data=verify_data,headers=headers)
    print("code_page-r=%s"%page_r.text)

def obtain_html_coolie(url):
    context = ssl._create_unverified_context()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': 'HttpOnly; WSYYTSESSION=LZfU6Vx9zMxOKDHdmAKE0rYuJRy0F1j_fah3C4aYiu936JX4gZwJ!-1857749737;'
        }
    dfcz_data={
        "ksny":"201701",
        "jzny":"201812",
        "glyhbh":"0622089504031565",
    }
    data = parse.urlencode(dfcz_data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    print("request.cookie=%s"%request.Request.get_header(req,"Cookie"))
    print("request.content-type=%s"%request.Request.get_header(req,"Content-Type"))
    page = request.urlopen(req,context=context).read()

    page = page.decode('utf-8')
    print("page-r=%s"%page.text)

def obtain_from_html(url,glyhbh,related_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': 'HttpOnly; WSYYTSESSION=t11PQ81NaFViUO6WNyNkf_GUtZ97TIRwgV4qM03sQr7rucUZyzeh!1944680279;'
        }

    dfcz_data={
        "ksny":"201812",
        "jzny":"201902",
        "glyhbh":glyhbh,
    }
    s = requests.Session()
    param_save_r = s.post(url, data=dfcz_data, headers=headers)
    #print("param_save_r=%s"%param_save_r.text)
    arr=crawlingDW(param_save_r.text,related_id)
    return arr

if __name__ == '__main__':
    rsa_js_path="./js/rsa.js"
    ctx = load_js(get_js(rsa_js_path))
    #zh=ctx.call("doRSAEncrypt", "87cbc10c-2e96-4c4a-96ff-b78ee974552f_c72cb115bbf6b39c0ba69d7dd2c21dca292f19cdfea8f13270a780b0f31ff3316f0a5a5695a2644db785c6e3374198914bcc6b26f8cec6ba643cdcb1824c48c1", "15121601911")
    #mm=ctx.call("doRSAEncrypt", "87cbc10c-2e96-4c4a-96ff-b78ee974552f_c72cb115bbf6b39c0ba69d7dd2c21dca292f19cdfea8f13270a780b0f31ff3316f0a5a5695a2644db785c6e3374198914bcc6b26f8cec6ba643cdcb1824c48c1", "sn123456789")

    #mock_login("https://95598.gz.csg.cn/yhdl.do","76hf","https://95598.gz.csg.cn/df/dldffx.do")
    #obtain_html_coolie("https://95598.gz.csg.cn/df/dldffx.do")
    #checkVerifyCode("h328","https://95598.gz.csg.cn/cvc.do")
    #exportExcel("https://95598.gz.csg.cn/df/dldffx.do","0622089504572150")
    obtain_from_html("https://95598.gz.csg.cn/df/dldffx.do","0605056013451352")
