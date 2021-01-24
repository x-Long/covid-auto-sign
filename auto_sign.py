# @ coding:utf8
# @ Author ：simonLTS
# @ email：liang_xaut@163.com
# @ Date: 2020/05/12
# @ Address: XAUT

import requests
import datetime
from requests.cookies import RequestsCookieJar
import re
import datetime
import time

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
import json


def getInfo(p1):

    response = requests.post(
        "https://app.xaut.edu.cn/uc/wap/login/check", data=p1)
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("UUkey", response.cookies["UUkey"])
    cookie_jar.set("eai-sess", response.cookies["eai-sess"])
    response2 = requests.post(
        "https://app.xaut.edu.cn/ncov/wap/default/index", cookies=cookie_jar)
    print(response2)
    def1 = re.findall('var def = (.*?);\n', response2.text)
    oldInfo = re.findall('oldInfo: (.*?),\n', response2.text)
    print(def1[0])
    print(oldInfo[0])
    return json.loads(def1[0]), json.loads(oldInfo[0])
    # json.loads(def1[0]),json.loads(oldInfo[0])


def changePosition(def1, oldInfo):

    def1["date"] = datetime.datetime.now().strftime('%Y%m%d')
    def1["address"] = oldInfo["address"]
    def1["area"] = oldInfo["area"]
    def1["province"] = oldInfo["province"]
    def1["city"] = oldInfo["city"]
    def1["geo_api_info"] = oldInfo["geo_api_info"]


def format1(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def commite(p1, def1, email):
    # 发送post请求
    response = requests.post(
        "https://app.xaut.edu.cn/uc/wap/login/check", data=p1)

    # print( response.cookies)

    # 先登录一下，登陆成功得到cookie
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("UUkey", response.cookies["UUkey"])
    cookie_jar.set("eai-sess", response.cookies["eai-sess"])

    # 抓取填写信息页面
    response2 = requests.post(
        "https://app.xaut.edu.cn/ncov/wap/default/index", cookies=cookie_jar)
    # print(response2.text)
    title = re.findall('var def = (.*?);\n', response2.text)

    # 修改所要提交信息的id
    def1["id"] = json.loads(title[0])["id"]

    # 提交信息
    response3 = requests.post(
        "https://app.xaut.edu.cn/ncov/wap/default/save", cookies=cookie_jar, data=def1)
    print(eval(response3.text)["e"])

    # 成功后发送邮件
    if (eval(response3.text)["e"] == 0):

        # 腾讯 阿里 基本不开放25端口，所以需要用基于ssl的smtp服务器
        # from_addr = "simonlts@163.com"
        # password  = "KXLFOUFTRMKNXDUJ"
        # # to_addr = "710450053@qq.com"
        # smtp_server = "smtp.163.com"
        # msg = MIMEText('hello，小助手刚刚已经帮您提交了疫情通~ ', 'plain', 'utf-8')
        # msg['From'] = format1('simonLTS <%s>' % from_addr)
        # msg['To'] = format1('<%s>' % email)
        # msg['Subject'] = Header('疫情通提交', 'utf-8').encode()
        # server = smtplib.SMTP(smtp_server, 25)
        # server.set_debuglevel(1)
        # server.login(from_addr, password)
        # server.sendmail(from_addr, email, msg.as_string())
        # server.quit()

        r = requests.get(
            "http://api.tianapi.com/txapi/tianqi/index?key=b94e1eda3886cba96d37aac1c2cc6d48&city=西安")
        r1 = requests.get(
            "http://api.tianapi.com/txapi/saylove/index?key=b94e1eda3886cba96d37aac1c2cc6d48")

        for i in range(0, 10):

            if json.loads(r.text)['newslist'][i]['date'] == datetime.datetime.now().strftime('%Y-%m-%d'):
                info = json.loads(r.text)['newslist'][i]
                break

        today = datetime.datetime.now()
        days = int((today - miss_time).days)

        email_info = "杨萱小朋友你好："+"\n\n\t今天是喜欢xxx的第"+str(days)+"天~"+"\n\n\t在这里倾心通知您，疫情通已经提交，特殊时期，口罩常备多喝水~ "+"\n\n\t另外，小喇叭为您奉上明日天气，祝您天天好心情~~"+"今天是"+info["date"]+"，天气："+info["weather"]+"，实时温度："+info["real"]+"，明天最高温度："+info[
            'highest']+"\n\n\t"+"小贴士给您说："+info["tips"]+"\n\n-♥--♥--♥--♥--♥--♥-\n\n"+"♥♥♥ 今日份情话To YX ♥♥♥"+"\n\n"+json.loads(r1.text)["newslist"][0]["content"]+"\n\nYou are the apple of my eyes~\n-♥--♥--♥--♥--♥--♥-\n\n"

        # 这里使用SMTP_SSL 默认使用465端口
        smtp = SMTP_SSL("smtp.163.com")
        smtp.set_debuglevel(1)

        smtp.ehlo("smtp.163.com")
        smtp.login("simonlts@163.com", "KXLFOUFTRMKNXDUJ")

        msg = MIMEText(email_info, "plain", "utf-8")
        msg["Subject"] = Header("疫情通打卡~", "utf-8")
        msg["from"] = "simonLTS"
        msg["to"] = email
        print(11)
        smtp.sendmail("simonlts@163.com", email, msg.as_string())
        smtp.quit()


def action(p1, def1, oldInfo, email):

    changePosition(def1, oldInfo)
    commite(p1, def1, email)


# h是设定的小时，m为设定的分钟
def main(h=0, m=1):

    while True:
        now = datetime.datetime.now()
        if now.hour == h and now.minute == m:
            action(p1_long, def1_long, oldInfo_long, email_long)
            # action(p1_某某某,def1_某某某,oldInfo_某某某,email_某某某)
        time.sleep(20)

if __name__ == '__main__':
	p1_long = {"username": "2191221082", "password": "lxlxxxxxxxx"}
	email_long = "710450053@qq.com"
	miss_time = datetime.datetime(2020, 6, 19)
	def1_long, oldInfo_long = getInfo(p1_long)
    main()
