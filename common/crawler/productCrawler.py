from bs4 import BeautifulSoup as bs
import requests
import csv
import re
from common.crawler.useOpengraph import productOpengraph

def opengraphParser(url):
    baseUrl = url
    response = requests.get(baseUrl,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

    soup = bs(response.content, "html.parser")

    ogs = soup.html.head.findAll(property=re.compile(r'^og'))
    products = soup.html.head.findAll(property=re.compile(r'^product'))

    for og in ogs:
        if og.has_attr(u'content'):
            print(og[u'content'])

    for item in products:
        if item.has_attr(u'content'):
            print(item[u'content'])

product = productOpengraph("http://m.earpearp.com/product/%EC%96%B4%ED%94%84%EC%96%B4%ED%94%84x%ED%8E%AD%EC%88%98dinner-tea-time-brown%ED%95%98%EB%93%9C/13198/category/1/display/2/")
print(product)

'''
images1 = soup.select('img[src*="product"]')
images2 = soup.select('img[src*="goods"]')
images3 = soup.select('img[class*="thumb"]')
images4 = soup.select('img[class*="Thumb"]')
images3 = soup.select('img[src*="thumb"]')
images4 = soup.select('img[src*="Thumb"]')
images5 = soup.find_all('picture')
images = images1 + images2 + images3 + images4 + images5
'''

'''
def productCroller(url):
    baseUrl = url
    response = requests.get(baseUrl,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    soup = bs(response.content, "html.parser")
    images1 = soup.select('img[class*="Logo"]')
    images2 = soup.select('img[class*="logo"]')
    images3 = soup.select('img[src*="logo"]')
    images4 = soup.select('img[src*="Logo"]')
    images5 = soup.select('h1[class*="logo"] img')
    images6 = soup.select('h1[class*="Logo"] img')
    images = images1 + images2 + images3 + images4 + images5 + images6
    if (len(images) == 0):
        svg = soup.select('svg')
        return svg[0] if len(svg) != 0 else '감지되지 않음'
    else:
        if len(images) != 0:
            return beautify_imgsrc(baseUrl, images[0]['src'])
        else:
            return '감지되지 않음'



def Is_have_og(url):
    baseUrl = url
    response = requests.get(baseUrl,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    soup = bs(response.content, "html.parser")
    og = ""
    og = soup.find("meta", property = "og:title")
    if len(og)>0:
        return og
    else:
        return "og 없어"



row_num = 0
with open('detail.csv', newline='') as csvfile:
    csv_data = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csv_data:
        if (row_num > 15):
            print("------------------", row[0], "------------------")
            opengraphParser(row[3])
        row_num +=1'''
