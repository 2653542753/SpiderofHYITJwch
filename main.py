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

    from_addr = '***'
    password = '***'
    to_addr = '***'
    smtp_server = '***'
    msg = MIMEText(title, 'plain', 'utf-8')
    msg['From'] = _format_addr('教务网爬虫 <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('教务网新闻更新', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


self = 2568
main1Page = 'http://jwch.hyit.edu.cn/index.aspx?menuid=29&type=articleinfo&lanmuid=121&infoid='
for k in range(1,10000):
    try:
        main_html = requests.get(main1Page + str(self))
        main_text = main_html.text
        soup = BeautifulSoup(main_text, "html.parser")
        final_title = soup.title.string
        title = final_title[:-9]
        self += 1
        SendMessage(title)
        sleep(900)
    except:
        break
