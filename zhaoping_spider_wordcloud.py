import urllib
import requests as rq
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import os
import random
from wordcloud import WordCloud, STOPWORDS

job_demand_list = [] # 保存职位要求url
# 获得职位要求url
def download(url):
    driver = webdriver.Firefox()
    driver.get(url) #访问链接
    pagesource = driver.page_source
    driver.close() #关闭
    soup = BeautifulSoup(pagesource, "lxml")
    find_url = soup.find_all(class_="contentpile__content__wrapper__item__info")
    for tmp in find_url:
        job_demand_list.append(tmp['href'])
mylist = ["https://sou.zhaopin.com/?p="+str(i)+"&jl=489&kw=python&kt=3" for i in range(1, 13)]
for url1 in mylist:
    download(url1)
    
# 获取职位要求页面
def get_demand(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    request = urllib.request.Request(url, headers=header)
    request.add_header("Connection", "keep-live")
    response = urllib.request.urlopen(request)
    source = response.read().decode('utf-8')
    return source

# 保存要求
f = open('work_demand.txt','w',encoding='utf-8')    #文件操作符 文件句柄 文件操作对象
for url2 in job_demand_list:
    pagesource2 = get_demand(url2)
    soup2 = BeautifulSoup(pagesource2, "lxml")
    job_ask = soup2.find_all(class_="pos-ul")
    if job_ask[0].children:
        if job_ask[0].find_all('span'):
            for child in job_ask[0].find_all('span'):
                if child.string:
                    print(child.string)
                    f.write(child.string)
        elif job_ask[0].find_all('p'):
            for child in job_ask[0].find_all('p'):
                if child.string:
                    print(child.string)
                    f.write(child.string)
        elif job_ask[0].find_all('div'):
            for child in job_ask[0].find_all('div'):
                if child.string:
                    print(child.string)
                    f.write(child.string)
    else:
        for job_ask_info in job_ask[0]:
            if job_ask_info.string:
                print(job_ask_info.string)
                f.write(job_ask_info.string)
f.close() #关闭文件

# 绘制词云，词云用的是网上开源项目github:https://github.com/amueller/word_cloud 
def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# read the mask image taken from
# http://www.stencilry.org/stencils/movies/star%20wars/storm-trooper.gif
mask = np.array(Image.open(path.join(d, "stormtrooper_mask.png")))

# movie script of "a new hope"
# http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html
# May the lawyers deem this fair use.
text = open(path.join(d, 'work_demand.txt'), encoding='utf-8').read()

# pre-processing the text a little bit
text = text.replace("岗位职责", "").replace("电子信息", "").replace("电气", "").replace("岗位方向", "")
text = text.replace("任职要求", "").replace("计算机", "").replace("自动化", "").replace("测控", "").replace("岗位要求", "")
text = text.replace("软件工程", "").replace("网络", "").replace("机电", "").replace("生仪", "").replace("任职要求", "")
text = text.replace("这既是挑战", "").replace("又是机遇", "").replace("大专及以上学历", "").replace("数学或英语等专业", "")
text = text.replace("签订正式", "").replace("劳动合同", "").replace("交通补贴", "").replace("定期加薪", "")
text = text.replace("福利待遇", "").replace("定期团建", "").replace("员工旅游", "").replace("免费培训", "")
text = text.replace("免费宿舍", "").replace("交通补助", "").replace("薪资待遇", "").replace("本职位为日本工作职位", "")
text = text.replace("简历请写明日语等级", "").replace("职业背景", "").replace("温馨提示", "").replace("高级工程师", "")
text = text.replace("在薪酬待遇方面", "").replace("远高于其他程序员", "").replace("感谢配合", "").replace("工作地点", "")

# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,random_state=1, font_path="simkai.ttf").generate(text)
# store default colored image
default_colors = wc.to_array()
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
wc.to_file("zhaoping.png")
plt.axis("off")
plt.figure()
plt.title("Default colors")
plt.imshow(default_colors, interpolation="bilinear")
plt.axis("off")
plt.show()