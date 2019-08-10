# coding = utf -8

import unittest
import time
from selenium import webdriver
import sys

sys.path.append('../..')
from util.mylogger import logger
from businessView.loginBusiness import LoginBusiness
from basefunc.basefunction import BaseOperation
from main.run_all import setDriver


class TestMain(unittest.TestCase):
    def setUp(self):
        logger.info('Test case running...')
        self.driver = setDriver()
        # 业务流引用
        self.busiNess = LoginBusiness(self.driver)
        # 基础函数引用
        self.baseFunc = BaseOperation(self.driver)
        self.imgs = []
        self.busiNess.openWeb()

    def test_01_user_login(self):
        """输入正确的信息登录系统"""
        try:
            self.busiNess.loginAction(1)
            time.sleep(2)
            assert self.baseFunc.readNotice() == '登录成功'
            time.sleep(2)
            assert self.baseFunc.is_exist('name', 'user') == False
            logger.info('Test case 01 pass')
        except AssertionError as e:
            self.imgs.append(self.driver.get_screenshot_as_base64())
            logger.info('Test case 01 fail' + e)
            raise

    def test_02_login_user_error(self):
        """输入错误的账号登录系统"""
        try:
            self.busiNess.loginAction(2)
            time.sleep(2)
            assert self.baseFunc.readNotice() == '账号不存在或密码错误'
            assert self.baseFunc.is_exist('name', 'user') == True
            logger.info('Test case 02 pass')
        except AssertionError as e:
            self.imgs.append(self.driver.get_screenshot_as_base64())
            logger.info('Test case 02 fail' + e)
            raise

    def test_03_login_pwd_error(self):
        """输入错误的密码登录系统"""
        try:
            self.busiNess.loginAction(3)
            time.sleep(2)
            assert self.baseFunc.readNotice() == '密码错误'
            assert self.baseFunc.is_exist('name', 'user') == True
            logger.info('Test case 03 pass')
        except AssertionError as e:
            self.imgs.append(self.driver.get_screenshot_as_base64())
            logger.info('Test case 03 fail' + e)
            raise

    def tearDown(self):
        self.baseFunc.closeWindow()


if __name__ == '__main__':
    unittest.main()
