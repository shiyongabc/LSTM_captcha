#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import requests
from predict import *
import os
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

#创建浏览器对象
driverPath="C://Program Files (x86)/Google/Chrome/Application/chromedriver"
driver = webdriver.Chrome(driverPath)
path = os.getcwd()  #项目所在路径

val_code_path = path + '/valcode.png'  #训练集-验证码所在路径

def obtainVerifyCode(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        #'Content-Type': 'application/x-www-form-urlencoded',
        #'Referer': 'https://95598.gz.csg.cn/df/zdcx.do',
        'Cookie': cookie
        }
    #获取验证码
    obtain_code_r = requests.get("https://95598.gd.csg.cn/ai.do?an=rnd_6564258381")
    f = open('valcode.png', 'wb')
    # 将response的二进制内容写入到文件中
    f.write(obtain_code_r.content)
    # 关闭文件流对象
    f.close()

def mock_click_login(url,zh,mm):
    driver.get(url)#"https://95598.gz.csg.cn/yhdl.do")

    # id="ptdl"是普通密码登陆，click() 是模拟点击
    driver.find_element_by_id("ptdl").click()
    #driver.find_element_by_xpath("//input[@id='ptdl']").check()

    # 输入账号
    driver.find_element_by_id("nctxt").send_keys(zh) #"15121601911")
    # 输入密码
    driver.find_element_by_id("mmtxt").send_keys(mm) #"sn123456789")

    # 获取验证码
    obtainVerifyCode("WSYYTSESSION="+driver.get_cookies()[1]['value']+";")
    print("val_code_path=%s"%val_code_path)
    predict_code=predictFromPath(val_code_path, "nmQX")
    print("predict_code=%s"%predict_code)
    # 输入验证码
    driver.find_element_by_id("yzmtxt").send_keys(predict_code)

    #登陆
    driver.find_element_by_id("dl1").click()

    # 获取当前页面Cookie
    #print(driver.get_cookies())
    print(driver.get_cookies()[1]['value'])

    #推辞渲染时间
    time.sleep(5)
    #print(driver.page_source)
    # dlero
    isError=driver.find_element_by_id("dlero").text
    print("isError=%s"%isError)
    while isError=="验证码输入不正确!":
        # 重新识别验证码
        obtainVerifyCode("WSYYTSESSION=" + driver.get_cookies()[1]['value'] + ";")
        print("val_code_path=%s" % val_code_path)
        predict_code = predictFromPath(val_code_path, "nmQX")
        print("predict_code=%s" % predict_code)
        # 输入验证码
        driver.find_element_by_id("yzmtxt").send_keys(predict_code)

        # 登陆
        driver.find_element_by_id("dl1").click()
        # 推辞渲染时间
        time.sleep(5)
        #print(driver.page_source)
        # dlero
        isError = driver.find_element_by_id("dlero").text
        print("isError=%s" % isError)

    # 关闭浏览器
    #driver.quit()

if __name__ == '__main__':
    mock_click_login("https://95598.gz.csg.cn/yhdl.do","15121601911","sn123456789")