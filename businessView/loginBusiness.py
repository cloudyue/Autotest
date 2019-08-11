# coding=utf-8

import sys

sys.path.append('../..')
from basefunc.basefunction import BaseOperation
from util.read_ini import ReadIni
from util.mylogger import logger


class LoginBusiness(BaseOperation):

    def __init__(self, driver):
        self.driver = driver
        self.efg = ReadIni(file_name='loginView.ini')
        self.cfg = ReadIni(isPageView=False)

    def openWeb(self):
        self.driver.get(self.cfg.Read_config('ALL_URL', 'test_url'))
        self.driver.maximize_window()

    def loginAction(self, line):
        """登录的操作"""
        data = self.get_csv_data('testLogin.csv', line)
        account = self.get_element('loginView', 'user', self.efg)
        pwd = self.get_element('loginView', 'pwd', self.efg)
        account.clear()
        account.send_keys(data[0])
        logger.info('输入测试数据' + data[0])
        pwd.clear()
        pwd.send_keys(data[1])
        logger.info('输入测试数据' + data[1])
        self.get_element('loginView', 'button', self.efg).click()
