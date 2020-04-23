# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:11:49 2020

@author: Harrison
"""
import os
import datetime
import pandas as pd 
import numpy as np
from WindPy import w
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import os
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import math
plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus']=False
#%%
pathroot=os.getcwd()
while True:
    #%%整理数据
    soup0=requests.get("http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56").text
    rawdata=str(soup0).split('{')[2].split('[')
    dayname=rawdata[2].split('"')[-6]
    s2n=rawdata[1].split('"')
    s2n=pd.DataFrame(s2n)
    s2n=s2n[s2n[0]!=',']
    s2n=s2n[0].str.split(',',5,True)
    s2n.columns=['时间','沪港通','沪港余额','深港通','深港通余额','北向总量']
    s2n=s2n.dropna()
    s2n=s2n.replace('-',np.nan)
    s2n.reset_index(inplace=True,drop=True)
    s2n[s2n.columns[1:]]=s2n[s2n.columns[1:]].astype('float')

#    fig = plt.figure(figsize=(10,5),linewidth=100)
    ax1 = plt.subplot(111)#2grid(111)#(3,4), (0,0), colspan=3,rowspan=3)
    plt.plot( s2n[['沪港通','深港通','北向总量']]/10000,linewidth=2)
    lastdata=s2n.dropna()
    y=lastdata.loc[lastdata.index[-1],['沪港通','深港通','北向总量']]/10000
    x=[lastdata.index[-1]]*3
    for i in range(3):
        plt.text(x[i],list(y)[i], list(y.apply(lambda x:'%.2f'%x))[i], ha='left', va= 'bottom',fontsize=12)
    plt.grid(linestyle='--', linewidth=0.5)
    plt.title('%s %s 北向资金(亿元),当前时间%s'%(dayname,s2n.loc[lastdata.index[-1],'时间'],str(datetime.datetime.now())[11:19]),fontproperties="SimHei",fontsize=14)
    #statdata['datetime']=statdata['time'].apply(lambda x: pd.to_datetime(x))
    ax1.set_ylim(math.floor(s2n[['北向总量','沪港通','深港通']].min().min()/10000/5-1)*5,math.ceil(s2n[['北向总量','沪港通','深港通']].max().max()/10000/5+1)*5)
    ax1.set_xlim(0,240)
    ax1.yaxis.set_major_locator(plt.MultipleLocator(5))
    #plt.ylabel('价差',fontproperties="SimHei",fontsize=14)
#    ax1.yaxis.set_major_locator(plt.MultipleLocator(5))
    a=list(range(0, 241, 15))
    plt.legend(['沪港通','深港通','北向总量'],prop={'family':'SimHei','size':12})#图例
    plt.xticks(a, s2n.loc[a,'时间'], rotation=90)
    timenow=time.time()-time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d'))
    plt.savefig(dayname+'.jpg',format='jpg',bbox_inches='tight',dpi=500)
    if (timenow>32400) & (timenow<55800):#16:30之后更新本日数据
        delaytime=10
    else:
        delaytime=57600
    plt.pause(delaytime)

    plt.cla()
    #plt.xlabel('日期',fontproperties="SimHei",fontsize=14)
    out = pd.ExcelWriter(pathroot+'\\南北向资金\\%s.xlsx'%dayname)
    s2n.to_excel(out, index=False,header=True)
    out.save()