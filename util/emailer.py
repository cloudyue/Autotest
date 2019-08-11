# coding=utf-8

import smtplib
import os
import mimetypes
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from util.read_ini import ReadIni
from util.mylogger import logger
from selenium import webdriver

email_host = "smtp.163.com"
send_user = ""
password = ""


def pre_send_mail(report_name):
    """发送邮件预处理"""
    cfg = ReadIni(isPageView=False, file_name="Email_config.ini")
    message = MIMEMultipart("related")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    to_addr = cfg.Read_config("Emailer", "To_addr")
    cc_addr = cfg.Read_config("Emailer", "Cc_addr")
    user_list = to_addr.split(',') + cc_addr.split(',')
    sub = "【请阅】固定资产UI自动化测试报告" + current_time
    user = send_user
    message['Subject'] = sub
    message['From'] = user
    message['To'] = to_addr
    message['Cc'] = cc_addr
    # 添加内容(或图片)到邮件正文中
    mail_content = """
            <p>您好，以下为固资平台UI自动化测试报告，详情请下载附件报告，推荐使用Chrome浏览器查看!</p>
            <p>ps:请将两个文件放在同一个目录下，再查看html报告,否则无法查看近十次测试统计图。</p>
            """
    # # 添加邮件正文信息
    mail_body = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    message.attach(mail_body)
    # 添加附件1
    ctype, encoding = mimetypes.guess_type(report_name[0])
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(report_name[0], 'rb'))[0], _subtype=subtype)
    att1.add_header("Content-Disposition", "attachment", filename=os.path.basename(report_name[0]))
    message.attach(att1)
    # 添加附件2
    ctype, encoding = mimetypes.guess_type(report_name[1])
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    att2 = MIMEImage((lambda f: (f.read(), f.close()))(open(report_name[1], 'rb'))[0], _subtype=subtype)
    att2.add_header("Content-Disposition", "attachment", filename=os.path.basename(report_name[1]))
    message.attach(att2)
    # 发送邮件
    server = smtplib.SMTP()
    server.connect(email_host)
    server.login(send_user, password)
    server.sendmail(user, user_list, message.as_string())
    server.close()


def new_report(test_report):
    """找出最新的测试报告"""
    # 列出目录下的所有文件和文件夹保存到lists
    lists = os.listdir(test_report)
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))
    # 获取最新的文件保存到file_new
    file_new = os.path.join(test_report, lists[-1])
    file_new2 = os.path.join(test_report, lists[-2])
    return file_new, file_new2


def send_email():
    """执行发送邮件"""
    report_path = os.path.dirname(os.path.dirname(__file__)) + '/report/'
    report_name = new_report(report_path)
    try:
        pre_send_mail(report_name)
        logger.info("自动化测试执行完成，邮件发送成功")
    except Exception as e:
        logger.info("邮件发送失败！" + e)



