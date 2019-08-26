#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-8-26 下午3:32
# @Author  : Aries
# @Site    : 
# @File    : taobao_buy.py
# @Software: PyCharm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time


class TaoBaoTimeBuy():
    def __init__(self):
        self.username = '13693391722'
        self.password = 'zk199006.,'
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.browser = webdriver.Chrome(executable_path="/home/gavin/PycharmProjects/taobao/chromedriver",
                                        options=self.options)
        self.wait = WebDriverWait(self.browser, 10)
        self.url = "https://login.taobao.com/member/login.jhtml"

    def login(self):
        ##打开淘宝登录页
        self.browser.get(self.url)
        ##等待密码登录选项出现
        password_login = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()
        # 等待 微博账号 出现
        taobao_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        # taobao_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username-field > #TPL_username_1')))
        taobao_user.send_keys(self.username)

        ##等待密码出现
        taobao_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        taobao_pwd.send_keys(self.password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()
        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                      '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)

    def buy(self,times,choose):
        if choose == 2:
            print("请手动勾选需要购买的商品")

        elif choose == 1:
            try:
                self.browser.find_element_by_id("J_SelectAll1").click()
            except:
                print("找不到购买按钮")

        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            ##对比事件，时间到的话就点击结算
            if now > times:
                try:
                    self.browser.find_element_by_link_text("结 算").click()
                    print("结算成功")
                    break
                except:
                    print("找不到结算按钮")
                    pass
        while True:
            try:
                self.browser.find_element_by_link_text('提交订单').click()
                now1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("抢购成功时间：%s" % now1)
                break
            except:
                print("再次尝试提交订单")




if __name__ == '__main__':
    times = '2019-08-26 18:36:15.000000'
    taobao = TaoBaoTimeBuy()

    taobao.login()
    choose = int(input("到时间自动勾选购物车请输入“1”，否则输入“2”："))
    taobao.buy(times=times,choose=choose)
