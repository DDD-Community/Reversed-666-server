from bs4 import BeautifulSoup as bs
import requests
import csv

def beautify_imgsrc(baseUrl, src):
    if (src.startswith('/') and not src.startswith('//')):
        return baseUrl + src
    if src.startswith('//'):
        return 'https:' + src
    if src.startswith('.'):
        return baseUrl + src
    return src

def logoCroller(url):
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

'''
row_num = 0
with open('products.csv', newline='') as csvfile:
    csv_data = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csv_data:
        if (row_num > 5 and row_num <15):
            print(row[0], logoCroller(row[2]))
        row_num +=1
'''