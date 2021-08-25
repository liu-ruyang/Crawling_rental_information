import decimal

import requests
from bs4 import BeautifulSoup
import js2xml
from lxml import etree
import pymysql


conn = conn = pymysql.connect(host="192.168.0.110",port=3306,user="root",password="123456",db="tenancy",charset="utf8")
cursor = conn.cursor()

page = 1
while page<=9:
    url = "https://zufang.leju.com/suzhou/house/n" + str(page) + "/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78"
    }
    resp = requests.get(url, headers=header)
    resp.encoding = "utf-8"
    demo = resp.text
    # print(demo)
    # soup = BeautifulSoup(demo,'lxml')
    # src = soup.select(".houseList_item")

    selector = etree.HTML(demo)

    mainInfo = selector.xpath('//div[@class="title_in"]//a/text()')
    community_name = selector.xpath('//span[@class="community_name"]//a/text()')
    buildTime = selector.xpath('//div[@class="address clearfix"]//span[3]/text()')
    updateTime_contactPerson = selector.xpath('//div[@class="agent_info clearfix"]//span/text()')  # 奇数是联系人，偶数是更新时间
    price = selector.xpath('//div[@class="price"]//span/text()')
    paymentMethod = selector.xpath('//div[@class="average_price"]/text()')
    roomURL = selector.xpath('//div[@class="title_in"]//a/@href')

    i = 0;
    while i < len(roomURL):
        print(mainInfo[i],
              community_name[i],
              buildTime[i],
              updateTime_contactPerson[2 * i],
              updateTime_contactPerson[2 * i + 1],
              price[i],
              paymentMethod[i],
              roomURL[i])
        cursor = conn.cursor()
        print(type(int(price[i])))
        cursor.execute(
            "insert into RoomsInfo(mainInfo,community_name,buildTime,updateTime,contactPerson,price,paymentMethod,roomUrl) values(%s,%s,%s,%s,%s,%s,%s,%s)",
            (mainInfo[i], community_name[i], buildTime[i], updateTime_contactPerson[2 * i],
             updateTime_contactPerson[2 * i + 1], decimal.Decimal(price[i]), (paymentMethod[i]).strip(), roomURL[i]))
        i += 1
    page+=1

conn.commit()
cursor.close()
conn.close()