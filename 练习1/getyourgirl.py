# -*-  coding = utf-8 -*-
# @Time : 2022/4/20 11:21
# @Autor : wsDongxz

import ssl
import os
import time
import re

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class GetYourGirl(object):

    def __init__(self, path=None):
        self.mainUrl = r"https://www.tu111.cc/plus/search.php?keyword={}"
        self.__headers = {
            'User-Agent':
                "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/78.0.3904.108Safari/537.36"
        }
        self.__context = ssl._create_unverified_context()
        self.basePath = path
        self.picSavePath = None
        self.jpgPageUrl = []
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
        # print(self.sehRspPageUrls)  # 查看所有的搜索页面url
        print('--------->'.ljust(15, ' '), '页面信息获取成功：共搜索得到{}页相关信息'.format(len(self.sehRspPageUrls)))

    def getPicLibInPage(self):
        print('--------->'.ljust(15, ' '), '准备获取每一页的图片库信息')
        time.sleep(3.5)
        if not self.sehRspPageUrls:
            print('--------->'.ljust(15, ' '), '错误！！！  无任何页面信息！')
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
            # print('rets', rets)
            for ret in rets:
                libInfoDict['picLibName'] = ret.img['alt'][:ret.img['alt'].find('<')-1]
                libInfoDict['picLibUrl'] = ret['href']
                # print('libInfoDict', libInfoDict)
                pageLibs.append(libInfoDict.copy())
                # print('pageLibs', pageLibs)
            pageLibCount += len(pageLibs)
            # print('pageLibs', pageCount, pageLibs)
            self.rspAllPagePicLibDict[pageCount] = pageLibs
            # print(self.rspAllPagePicLibDict)
            print('--------->'.ljust(15, ' '), '成功获取第{}/{}页的图片库信息：获取图片库数量 {} 个'.format(pageCount, len(self.sehRspPageUrls), len(pageLibs)))
            pageCount += 1
            time.sleep(3.5)
        # print(len(self.rspAllPagePicLibDict))
        # print(self.rspAllPagePicLibDict.keys())
        print('--------->'.ljust(15, ' '), '图片库信息获取成功：共获取{}/{}页, 获取图片库{}个'.format(pageCount-1, len(self.sehRspPageUrls), pageLibCount-1))
        # print(self.rspAllPagePicLibDict[1])

    def getLibAllJpg(self, jpgSavePath=None, jpgLibUrl=None, libNo=0):
        '''
        :param jpgSavePath:  Jpg文件的保存路径
        :param jpgLibUrl: ： JpgLib的Url地址，每一个Url地址下面包含很多页面
        :return: None
        '''
        self.jpgPageUrl = []
        sehReq = urllib.request.Request(url=jpgLibUrl, headers=self.__headers)
        response = urllib.request.urlopen(url=sehReq, context=self.__context)
        jpgLibSoup = BeautifulSoup(markup=response, features='lxml')
        baseUrl = jpgLibUrl[: jpgLibUrl.rfind('.')]
        # print(baseUrl)
        rets = jpgLibSoup.select(selector=('html>body>.content_img>.pages>a'))  # 页面信息
        pageNoStr = '.*?([0-9]{1,3})页'
        reObj = re.compile(pattern=pageNoStr)
        reRet = reObj.findall(rets[0].text.strip())[0]
        self.jpgPageUrl = [baseUrl+'_'+str(i)+'.html' for i in range(2, int(reRet) + 1)]
        self.jpgPageUrl.insert(0, jpgLibUrl)   # 该JpgLib下面的所有页面Url
        time.sleep(3.5)
        # print(self.jpgPageUrl)
        # print('==============')
        pageCount = 1
        for page in self.jpgPageUrl:
            # print('=================================')
            print('--------->'.ljust(15, ' '), '获取库 {} 第 {} 页图片中... ...'.format(libNo, pageCount))
            self.__getJpgForUrl(page, jpgSavePath)
            time.sleep(3.5)  # 管理员设置3.5s访问一下
            pageCount += 1

    def  __getJpgForUrl(self, jpgPageUrl=None, jpgSavePath=None):
        sehReq = urllib.request.Request(url=jpgPageUrl, headers=self.__headers)
        response = urllib.request.urlopen(url=sehReq, context=self.__context)
        jpgLibSoup = BeautifulSoup(markup=response, features='lxml')
        rets = jpgLibSoup.select(selector=('html>body>.content_img>.content>img'))
        for ret in rets:
            imgFileUrl = ret['src']
            jpgReq = urllib.request.Request(url=imgFileUrl, headers=self.__headers)
            response = urllib.request.urlopen(url=jpgReq, context=self.__context)
            jpgFileName = imgFileUrl[imgFileUrl.rfind('/') + 1 :]
            jpgFilePath = os.path.join(jpgSavePath, jpgFileName)
            # print('jpgFilePath', jpgFilePath)
            with open(jpgFilePath, 'wb') as jpgObj:
                jpgObj.write(response.read())

    def __creatPicFilePath(self, modelName=None, picLibName=None):

        self.picSavePath = os.path.join(self.basePath, self.sehModel)
        if not os.path.exists(self.picSavePath):
            print('--------->'.ljust(15, ' '), '准备创建文件夹')
            os.makedirs(self.picSavePath)
            print('--------->'.ljust(15, ' '), '在"{}"下创建文件夹 {} 成功'.format(self.basePath, self.sehModel))
        picPath = os.path.join(self.picSavePath, picLibName)
        bgPicPath = os.path.join(self.picSavePath, 'bgPic')

        if not os.path.exists(picPath):
            os.makedirs(picPath)
            print('--------->'.ljust(15, ' '), '在"{}"下创建文件夹 {} 成功'.format(self.sehModel, picLibName))

        if not os.path.exists(bgPicPath):
            os.makedirs(bgPicPath)
            print('--------->'.ljust(15, ' '), '在"{}"下创建文件夹 {} 成功'.format(self.sehModel, 'bgPic'))
        return picPath


    def getJpgFromPage(self, startPage=1, endPage=1):
        # 处理数据页信息
        if startPage < 1:
            startPage = 1
        if endPage > len(self.sehRspPageUrls):
            endPage = len(self.sehRspPageUrls)
        if endPage < startPage:
            endPage = startPage

        # 获取数据也Url

        for page in range(startPage, endPage+1):
            # 得到每一页的图片库信息：库名字、库链接
            pageUrlLibs = self.rspAllPagePicLibDict[page]
            # print(pageUrlLibs)
            # print(type(pageUrlLibs))
            # print('len(pageUrlLibs)', len(pageUrlLibs))
            # print('=======================')
            libCount = 1
            for lib in pageUrlLibs:
                # 获取Pic libs的名字与url地址
                # print('=======================')
                print('--------->'.ljust(15, ' '), '正在处理第 {} 页，图片库 {}'.format(page, libCount))
                # print(lib['picLibName'])
                # print(lib['picLibUrl'])
                jpgLibName = str(page) + "_" + str(libCount) + '_' + lib['picLibName']
                jpgLibUrl = lib['picLibUrl']
                jpgLibSavePath = self.__creatPicFilePath(modelName=self.sehModel, picLibName=jpgLibName)
                self.getLibAllJpg(jpgLibSavePath, jpgLibUrl, libCount)
                libCount += 1
                # print('jpgLibSavePath', jpgLibSavePath)

    def bgSelect(self):
        pass


    def run(self, startPage=1, endPage=1):
        self.getSearchUrl()
        self.getAllSehPageUrl()
        self.getPicLibInPage()
        self.getJpgFromPage(startPage, endPage)


if __name__ == '__main__':
    print('==============================')
    path = r"E:\myProject\Code\Python\spider\spiderEdu\0.base"
    myApp = GetYourGirl(path=path)
    myApp.run()
