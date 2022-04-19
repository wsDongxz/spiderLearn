# -*-  coding = utf-8 -*-
# @Time : 2022/4/19 17:57
# @Autor : wsDongxz
import urllib.request
import ssl
import urllib.parse
import re
from bs4 import BeautifulSoup

# https://www.tu111.cc/plus/search.php?keyword=%D1%EE%B3%BF%B3%BF
# https://www.tu111.cc/plus/search.php?keyword=%CF%C4%C4%AD%C4%AD
#  =================== 构建url =============
baseUrl = r"https://www.tu111.cc/plus/search.php?keyword={}"
# print(baseUrl.format("杨晨晨"))
# urlPrc = urllib.parse.unquote('https://www.tu111.cc/plus/search.php?keyword=%D1%EE%B3%BF%B3%BF', encoding='gbk')

# strName = input("请输入要搜索的名字：")
strName = '杨晨晨'
url_quote = urllib.parse.quote(strName, encoding='gbk')
newUrl = baseUrl.format(url_quote)
print("newUrl：".ljust(10, ' '), newUrl)
'''
response = urllib.request.urlopen(url_quote)
print(response.read().decode('gbk'))
'''
#  =================== 发送请求 =============
myContent = ssl._create_unverified_context()
headers = {'User-Agent':
                "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/78.0.3904.108Safari/537.36"
            }
userRequeset = urllib.request.Request(url=newUrl, headers=headers)
response = urllib.request.urlopen(url=userRequeset, context=myContent)
responseStr = response.read().decode('gbk')
print(responseStr)

# <a href="()_blank">.*？<img src=() .*?</a>
# <a href="https://www.tu111.cc/doyu/[0-9]{}/43197.html" target="_blank">
# <a href='/plus/search.php?keyword=%D1%EE%B3%BF%B3%BF&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=30&typeid=0&TotalResult=391&PageNo=2'>2</a><a href='/plus/search.php?keyword=%D1%EE%B3%BF%B3%BF&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=30&typeid=0&TotalResult=391&PageNo=3
partenStr = "<a href='/plus/search.php?keyword=%D1%EE%B3%BF%B3%BF&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=30&typeid=0&TotalResult=391&PageNo=2'>2</a><a href='/plus/search.php?keyword=%D1%EE%B3%BF%B3%BF&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=30&typeid=0&TotalResult=391&PageNo=3"
re_obj = re.compile(pattern=partenStr, flags=re.S)
result = re_obj.findall(responseStr)
print(result)
print(len(result))

# <a href="/plus/search.php?keyword={};.*?PageNo=[0-9]{1,2}]">

pagePartenStr = 'a href=.?search.*?keyword=%D1%EE%B3%BF%B3%BF.*?PageNo=4'
print(pagePartenStr)
re_obj = re.compile(pattern=pagePartenStr, flags=re.S)
result = re_obj.findall(responseStr)
print(result)
print(len(result))
