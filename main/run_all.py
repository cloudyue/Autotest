# coding = utf-8

import unittest
import os
import datetime
from selenium import webdriver
import sys

sys.path.append("../..")
from util import HTMLTestRunner_Chart
from util.emailer import send_email
from util.mylogger import logger


def setDriver():
    """初始化driver"""
    #############################
    # 配置chrome浏览器无界面测试
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # driver = webdriver.Chrome(chrome_options=option)
    #############################
    # 启用谷歌浏览器
    driver = webdriver.Chrome()
    # 启用火狐浏览器
    # driver = webdriver.Firefox()
    return driver


class RunAll(unittest.TestCase):

    def test_all(self):
        """
        @note:执行testSuite目录下以test开头的测试用例
        """
        # 执行用例路径
        logger.info('')
        base_path = os.path.dirname(os.path.dirname(__file__))
        case_path = os.path.join(base_path, "testSuite")
        suite = unittest.defaultTestLoader.discover(case_path, 'test*.py')
        # 写入测试报告
        # report_name = "Report_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".html"
        report_name = "JC_AutoTest_Report.html"
        file_path = os.path.join(base_path + "/report/" + report_name)
        report_title = "精臣固定资产自动化测试报告"
        with open(file_path, 'wb') as test_report:
            runner = HTMLTestRunner_Chart.HTMLTestRunner(stream=test_report, title=report_title, verbosity=2, retry=0,
                                                         save_last_try=True)
            runner.run(suite)
        # 发送邮件
        # send_email()


if __name__ == '__main__':
    unittest.main()
