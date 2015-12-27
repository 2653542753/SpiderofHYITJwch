from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from time import sleep
from bs4 import BeautifulSoup
import requests
import smtplib


def SendMessage(title):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = '****'
    password = '****'
    to_addr = '****'
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

def analyiseWeb(WebNum):
    mainpage = 'http://jwch.hyit.edu.cn/index.aspx?menuid=29&type=articleinfo&lanmuid=121&infoid='
    CheckNum = 0
    for i in range(1,10000):
        try:
            main_html = requests.get(mainpage + str(WebNum))
            main_text = main_html.text
            soup = BeautifulSoup(main_text, "html.parser")
            final_title = soup.title.string
            title = final_title[:-9]
            WebNum += 1
            print(title + str(WebNum))
            #SendMessage(title)
            sleep(1)
        except:
            print('无法查询到，进行下一次查询' + str(WebNum))
            WebNum += 1
            CheckNum += 1
            if (CheckNum > 3):
                CheckNum = 0
                break
            else:
                continue

print(analyiseWeb(2590))