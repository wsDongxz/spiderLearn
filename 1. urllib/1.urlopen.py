# -*-  coding = utf-8 -*-
# @Time : 2022/4/19 16:16
# @Autor : wsDongxz

import urllib.request

# 注意一个完整的URL通常以'/ '结尾，当输入URL时记得补充斜线
myUrl = r'https://www.tu111.cc/'
picUrl = r'https://pic.tu111.cc/jpge/2022/allimg/220411/11164449-28-R38.jpg'
# 返回值response为服务器响应对象
response = urllib.request.urlopen(url=myUrl)
picResponse = urllib.request.urlopen(url=picUrl)
# 解码
print(response.read().decode("gbk"))
with open(r'..\File\meinv.jpg', 'wb') as f:
    f.write(picResponse.read())
