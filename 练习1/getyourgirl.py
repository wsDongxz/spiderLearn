# -*-  coding = utf-8 -*-
# @Time : 2022/4/20 11:21
# @Autor : wsDongxz

import ssl
import os
import time

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class GetYourGirl(object):

    def __init__(self):
        self.mainUrl = r"https://www.tu111.cc/plus/search.php?keyword={}"
        self.__headers = {
            'User-Agent':
                "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/78.0.3904.108Safari/537.36"
        }
        self.__context = ssl._create_unverified_context()
        self.sehUrl = None
        self.sehModel = None
        self.sehRspPageUrls = []  # 所有搜索 页面的 url ，
        self.rspAllPagePicLibDict = {}  # {pageNo: [(picLibName1, picLibUrl1), (picLibName2, picLibUrl2), ... ]}
        self.picLibDict = {}  # {PicLibName1: [picUrl1, picUrl2, ...], PicLibName1: [picUrl1, picUrl2, ...]}

    def getSearchUrl(self, modelName='杨晨晨'):
        self.sehModel = modelName
        print('--------->'.ljust(15, ' '), '正在生成Url')
        self.sehUrl = self.mainUrl.format(urllib.parse.quote(modelName, encoding='gbk'))
        if self.sehUrl:
            print('--------->'.ljust(15, ' '), '生成Utl成功')
            return True
        print('--------->'.ljust(15, ' '), '生成Utl失败')
        return False

    def getAllSehPageUrl(self):
        print('--------->'.ljust(15, ' '), '正在获取所有搜索得到的页面信息......')
        if not self.sehUrl:
            return False
        sehReq = urllib.request.Request(url=self.sehUrl, headers=self.__headers)
        response = urllib.request.urlopen(url=sehReq, context=self.__context)
        sehSoup = BeautifulSoup(markup=response, features='lxml')
        # print(sehSoup.prettify())
        srhAllPageHtml = sehSoup.select(selector=('html>body>.m>.pages a'))
        pageHtml = []
        # 原始页面信息
        for page in srhAllPageHtml:
            if 'href' in page.prettify():
                # print(page)
                pageHtml.append(page)
        # 保留有效页码，去掉下一页，末页
        self.sehRspPageUrls = []
        for page in pageHtml:
            if not (page['href'] in self.sehRspPageUrls):
                self.sehRspPageUrls.append(page['href'])

        # 整理得到真实的页面Html
        urlPre = r'https://www.tu111.cc/'
        #  serchRageHtmls真实的页面Html，所有搜索相关的页面
        self.sehRspPageUrls = [urlPre + url for url in  self.sehRspPageUrls]
        self.sehRspPageUrls.insert(0, self.sehUrl)
        print('--------->'.ljust(15, ' '), '页面信息获取成功：共搜索得到{}页相关信息'.format(len(self.sehRspPageUrls)))

    def getPicLibInPage(self):
        print('--------->'.ljust(15, ' '), '准备获取每一页的图片库信息')
        time.sleep(3.5)
        if not self.sehRspPageUrls:
            return False
        pageCount = 1
        pageLibCount = 0
        # 依次遍历所有的返回页面
        for url in self.sehRspPageUrls:
            print('--------->'.ljust(15, ' '), '开始获取第{}/{}页的图片库信息'.format(pageCount, len(self.sehRspPageUrls)))
            # print('url'.ljust(10, ' '), url)
            pageReq = urllib.request.Request(url=url, headers=self.__headers)
            response = urllib.request.urlopen(url=pageReq, context=self.__context)
            # print('code'.ljust(10, ' '), response.getcode())
            pageSoup = BeautifulSoup(markup=response, features='lxml')
            # 该标签下包含 picLib 以及其 名字
            rets = pageSoup.select(selector=('html>body>.m>.ind2>ul>li>a'))  # <class 'bs4.element.ResultSet'>
            pageLibs = []

            libInfoDict = {'picLibName': None, 'picLibUrl': None}
            # 提取图片库名字及链接
            for ret in rets:
                # print(ret['href'])
                # print(ret.img['alt'][:ret.img['alt'].find('<')-1])
                libInfoDict['picLibName'] = ret.img['alt'][:ret.img['alt'].find('<')-1]
                libInfoDict['picLibUrl'] = ret['href']
                pageLibs.append(libInfoDict)
            pageLibCount += len(pageLibs)
            self.rspAllPagePicLibDict[pageCount] = pageLibs
            print('--------->'.ljust(15, ' '), '成功获取第{}/{}页的图片库信息：获取图片库数量 {} 个'.format(pageCount, len(self.sehRspPageUrls), len(pageLibs)))
            pageCount += 1
            time.sleep(3.5)
        # print(len(self.rspAllPagePicLibDict))
        # print(self.rspAllPagePicLibDict.keys())
        print('--------->'.ljust(15, ' '), '图片库信息获取成功：共获取{}/{}页, 获取图片库{}个'.format(pageCount, len(self.sehRspPageUrls), pageLibCount-1))
        # print(self.rspAllPagePicLibDict[1])

    def getJpgFromPage(self, startPage=1, endPage=10):
        # 数据有效性
        if startPage < 1:
            startPage = 1
        if endPage > len(self.sehRspPageUrls):
            endPage = len(self.sehRspPageUrls)
        pass

    def run(self):
        self.getSearchUrl()
        self.getAllSehPageUrl()
        self.getPicLibInPage()


if __name__ == '__main__':
    print('==============================')
    myApp = GetYourGirl()
    # myApp.run()