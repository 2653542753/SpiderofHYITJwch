from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from time import sleep
from bs4 import BeautifulSoup
import requests
import smtplib
import time


def SendMessage(title):  # 发送邮件
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = 'psxhero@163.com'
    password = 'bwdbtxdaurpudjhs'
    to_addr = '15996155035@139.com'
    smtp_server = 'smtp.163.com'
    msg = MIMEText(title, 'plain', 'utf-8')
    msg['From'] = _format_addr('爬虫提醒 <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('教务网新闻更新', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def loop(WebNum):  # 解析网页并且每10秒钟自动执行一次查询功能
    while True:
        main_page = 'http://jwch.hyit.edu.cn/index.aspx?menuid=29&type=articleinfo&lanmuid=121&infoid='
        checksum = 0
        for i in range(1, 10000):
            try:
                main_html = requests.get(main_page + str(WebNum))
                main_text = main_html.text
                soup = BeautifulSoup(main_text, "html.parser")
                final_title = soup.title.string
                title = final_title[:-9]
                WebNum += 1
                print(title + str(WebNum-1))
                #SendMessage(title)
                sleep(1)
            except:  # 发现非法网页,无法解析
                print('无法查询到，进行下一个网页查询' + str(WebNum))
                WebNum += 1
                checksum += 1
                if checksum > 3:  # 若连续3个网页无法解析，认为已经获取到最新的消息，退出功能
                    checksum = 0
                    WebNum -= 4
                    print('本次函数运行结束！')
                    break
                else:
                    continue  # 若小于3个网页，继续进行解析
        time.sleep(300)  # 停止10分钟后再次执行该函数
    time.sleep(600)


print(loop(2594)) # 2594为淮阴工学院教务处的某一则新闻

'''
注释
main_page：新闻地址前缀
WebNum: 新闻ID
main_html：新闻网页
main_text：新闻全部文字
final_title：新闻标题
title：过滤后的得到的标题
from_addr：发件人信箱
password = 邮箱密码
to_addr = 收件人信箱
smtp_server = smtp域名（一般格式为：smtp.你邮箱域名，例如smtp.163.com）

特别注意！如果使用163信箱，请确保开启了smtp服务,同时输入的是163提供的smtp邮箱密码，非登陆163邮箱的密码！
'''