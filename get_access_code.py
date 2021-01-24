# # @ coding:utf8
# # @ Author ：simonLTS
# # @ email：liang_xaut@163.com
# # @ Date: 2020/05/12
# # @ Address: XAUT

import requests
import sys

response=requests.post("https://app.xaut.edu.cn/uc/wap/login/check",data={"username":sys.argv[1],"password":sys.argv[2]})
	#获取返回的json数据
print(response.text)
