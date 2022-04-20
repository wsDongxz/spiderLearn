# -*-  coding = utf-8 -*-
# @Time : 2022/4/19 17:57
# @Autor : wsDongxz
import urllib.request
import ssl
import urllib.parse
import re
from bs4 import BeautifulSoup
import time

#  =================== 构建url =============
baseUrl = r"https://www.tu111.cc/plus/search.php?keyword={}"
# strName = input("请输入要搜索的名字：")
strName = '杨晨晨'
url_quote = urllib.parse.quote(strName, encoding='gbk')
# 用于请求的url
newUrl = baseUrl.format(url_quote)
print("newUrl：".ljust(10, ' '), newUrl)

#  =================== 发送GET 请求  搜索 =============
myContent = ssl._create_unverified_context()
headers = {'User-Agent':
                "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/78.0.3904.108Safari/537.36"
            }
userRequeset = urllib.request.Request(url=newUrl, headers=headers)
response = urllib.request.urlopen(url=userRequeset, context=myContent)
'''
responseStr = response.read().decode('gbk')
print(responseStr)
'''

# ================ 当前页面的所有相关图片链接 ===================
picHtmls = []
soup = BeautifulSoup(markup=response, features='lxml')
# print(soup.prettify())
# print('soup', type(soup))
ret = soup.select(selector=('html>body>.m>.ind2>ul>li>a'))
# print(len(ret))

for url in ret:
    picHtmls.append(url['href'])
    # print(url['href'])


# =============== 所有页面 =============================
retPage = soup.select(selector=('html>body>.m>.pages a'))
pageHtml = []
# 原始页面信息
for page in retPage:
    if 'href' in page.prettify():
        # print(page)
        pageHtml.append(page)
# 保留有效页码，去掉下一页，末页
serchRageHtmls = []
for page in pageHtml:
    if not page['href'] in serchRageHtmls:
        serchRageHtmls.append(page['href'])
    # print(page['href'])
    # print(type(page['href']))  # str
# print(serchRageHtmls)
# print(len(serchRageHtmls))
# 整理得到真实的页面Html
urlPre = r'https://www.tu111.cc/'
#  serchRageHtmls真实的页面Html，所有搜索相关的页面
serchRageHtmls = [urlPre + url for url in serchRageHtmls]

# =============== 开始按照页面爬取 ================
serchPage = 1
demoUrl = picHtmls[0]
print('demoUrl:'.ljust(10, ' '), demoUrl)
picReq = urllib.request.Request(url=demoUrl, headers=headers)
response = urllib.request.urlopen(url=picReq, context=myContent)
# 所有图片页面的基础地址
basePicPageUrl = response.geturl()[:response.geturl().rfind('/')+1]
# print('basePicPageUrl', basePicPageUrl)
soup = BeautifulSoup(markup=response, features='lxml')
# print(soup.prettify())
retJpgTag = soup.select(selector=('html>body>.content_img>.content>img'))
retjpgPage = soup.select(selector=('html>body>.content_img>.pages>a'))
print(len(retJpgTag))

for jpgHtml in retJpgTag:
    # jpgHtml['src'] 真实的图片地址, 开始保存图片
    # print(jpgHtml['src'])
    # 图片名字
    jpgUrl = jpgHtml['src']
    jpgName = jpgUrl[jpgUrl.rfind('/')+1:]
    # print('jpgName'.ljust(10, ' '), jpgName)
    jpgReq = urllib.request.Request(url=jpgUrl, headers=headers)
    response = urllib.request.urlopen(url=jpgReq, context=myContent)
    # E:\myProject\Code\Python\spider\spiderEdu\练习1\img
    picFile = r".\\img\\" + jpgName
    with open(picFile, 'wb') as obj:
        obj.write(response.read())
        print(jpgName.ljust(20, ' '), "save success")


print(len(retjpgPage))


