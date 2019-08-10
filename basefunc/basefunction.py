# coding = utf-8

import csv
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

sys.path.append('../..')
from util.mylogger import logger
from util.read_ini import ReadIni


class BaseOperation:
    """系统操作基础类"""

    def __init__(self, driver):
        self.driver = driver
        self.cfg = ReadIni(isPageView=False)
        self.efg = ReadIni(file_name='local_element.ini')

    def OpenSystem(self):
        """AW: 登录固定资产系统"""
        try:
            efg = ReadIni(file_name='loginView.ini')
            url = self.cfg.Read_config('ALL_URL', 'test_url')
            user = self.cfg.Read_config('test_account', 'user_name')
            pd = self.cfg.Read_config('test_account', 'pass_word')
            self.driver.get(url)
            self.driver.maximize_window()
            account = self.get_element('loginView', 'user', efg)
            pwd = self.get_element('loginView', 'pwd', efg)
            account.clear()
            account.send_keys(user)
            logger.info('输入账号信息')
            pwd.clear()
            pwd.send_keys(pd)
            logger.info('输入密码信息')
            self.get_element('loginView', 'button', efg).click()
            time.sleep(5)
            try:
                self.closeNotice()
                time.sleep(3)
                logger.info('关闭公告弹窗')
                logger.info('成功登陆系统')
            except:
                logger.info('无弹窗，成功登陆系统')
        except Exception as e:
            logger.info('系统登陆失败' + e)
##########################################################################

    def closeNotice(self):
        """系统公告通知的关闭"""
        btw = self.get_Elements('BaseControl', 'close_notice', self.efg, 5).click()
        return btw


    def closeWindow(self):
        """关闭系统窗口"""
        self.driver.close()
        self.driver.quit()
        logger.info('Test case finished, system close...')
##########################################################################
    def topView(self):
        """点击功能列表首页"""
        btw = self.get_Elements('BaseControl', 'funclist', self.efg, 0).click()
        return btw

    def stoRage(self):
        """点击功能列表资产入库"""
        btw = self.get_Elements('BaseControl', 'funclist1', self.efg, 1).click()
        return btw

    def productMgr(self):
        """点击功能列表资产管理"""
        btw = self.get_Elements('BaseControl', 'funclist2', self.efg, 0).click()
        return btw

    def checkMgr(self):
        """点击功能列表盘点管理"""
        btw = self.get_Elements('BaseControl', 'funclist1', self.efg, 9).click()
        return btw

    def analyzeReport(self):
        """点击功能列表分析报表"""
        btw = self.get_Elements('BaseControl', 'funclist2', self.efg, 1).click()
        return btw

    def settingMgr(self):
        """点击功能列表分析报表"""
        btw = self.get_Elements('BaseControl', 'funclist2', self.efg, 2).click()
        return btw

########################################################################

    def readNotice(self):
        """获取通知、提示"""
        res = self.get_element('BaseControl', 'warning', self.efg).text
        return res

########################################################################

    def get_element(self, section, key, efg):
        """@note:获取配置文件中的页面元素，@section:元素模块，@key:元素id,name,classname,xpath，@efg:页面元素，@return:返回找到的元素"""
        data = efg.Read_config(section, key)
        by = data.split('>')[0]
        value = data.split('>')[1]
        logger.info("locate by:[" + by + "] value:[" + value + ']')
        try:
            if by == 'id':
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id(value))
            elif by == 'name':
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_name(value))
            elif by == 'classname':
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name(value))
            else:
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(value))
        except Exception:
            raise

    def get_Elements(self, section, key, efg, index):
        """@note:获取配置文件中的页面元素，@section:元素模块，@key:元素id,name,classname,xpath，@efg:页面元素，@index:元素索引，@return 返回找到的元素集合"""
        data = efg.Read_config(section, key)
        by = data.split('>')[0]
        value = data.split('>')[1]
        logger.info("locate by:[" + by + "] value:[" + value + '] is number ' + str(index + 1))
        try:
            if by == 'id':
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_id(value)[index])
            elif by == 'name':
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_name(value)[index])
            elif by == 'classname':
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_class_name(value)[index])
            else:
                return WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_xpath(value)[index])
        except Exception:
            raise

    def is_exist(self, method, exp):
        """@note: 判断元素是否存在, @method:定位方法, @exp:元素路径或名称"""
        try:
            self.driver.find_element(by=method, value=exp)
            logger.info('查找到%s元素' % exp)
        except NoSuchElementException:
            logger.info('未找到%s元素' % exp)
            return False
        else:
            return True

    def scoll(self, element, index=None):
        """@note:滚动页面, @path:滚动时参考的元素，路径或者元素对象,@index:up 元素在最上，down 元素在最下"""
        if index == 'up':
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        elif index == 'down':
            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        else:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        logger.info('页面滚动到选中元素位置')

########################################################################

    def get_csv_data(self, filename, line):
        """读取.csv文件中的数据"""
        path = os.path.dirname(os.path.dirname(__file__))
        data_path = path + '/data/' + filename
        logger.info('读取%s中的测试数据' % filename)
        with open(data_path, 'r', encoding='utf-8') as p:
            reader = csv.reader(p)
            for index, row in enumerate(reader, 1):
                if index == line:
                    return row

    def save_csv_data(self, filename, data):
        """保存数据到.csv文件中"""
        path = os.path.dirname(os.path.dirname(__file__))
        data_path = path + '/data/' + filename
        logger.info('写入数据到%s中' % filename)
        with open(data_path, 'w', encoding='utf-8', newline='') as p:
            csv_write = csv.writer(p)
            for i in data:
                csv_write.writerow(i)
            logger.info('数据保存成功')
#########################################################################
