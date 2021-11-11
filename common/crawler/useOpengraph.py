import re
from bs4 import BeautifulSoup
import requests

class productOpengraph(dict):
    """
    """

    required_attrs = ['image', 'title',  'price_currency', 'price_amount']

    def __init__(self, url=None, scrape=True, **kwargs):
        # scrape == True면 missing arguments를 body에서 스크랩해 가져온다.
        self.scrape = scrape
        self._url = url

        for k in kwargs.keys():
            self[k] = kwargs[k]

        dict.__init__(self)

        if url is not None:
            self.fetch(url)

    def __setattr__(self, name, val):
        self[name] = val

    def __getattr__(self, name):
        return self[name]

    def fetch(self, url):
        """
        """
        response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        soup = BeautifulSoup(response.content, "html.parser")
        return self.parser(soup)

    def parser(self, doc):
        """
        """
        ogs = doc.html.head.findAll(property=re.compile(r'^og'))
        for og in ogs:
            if og.has_attr(u'content'):
                self[og[u'property'][3:]]=og[u'content']

        products = doc.html.head.findAll(property=re.compile(r'^product'))
        for product in products:
            if product.has_attr(u'content'):
                self[product[u'property'][8:].replace(':', '_')]=product[u'content']
        
        # og태그로부터 모든 속성을 받아오지 못하면, body를 스크랩한다.
        if not self.is_valid() and self.scrape:
            for attr in self.required_attrs:
                if not self.valid_attr(attr):
                    try:
                        self[attr] = getattr(self, 'scrape_%s' % attr)(doc)
                    except AttributeError:
                        pass

    def valid_attr(self, attr):
        return self.get(attr) and len(self[attr]) > 0

    def is_valid(self):
        return all([self.valid_attr(attr) for attr in self.required_attrs])

    def scrape_image(self, doc):
        images = [dict(img.attrs)['src']
            for img in doc.html.body.findAll('img')]

        if images:
            return images[0]

        return u''

    def scrape_title(self, doc):
        return doc.html.head.title.text

    def scrape_type(self, doc):
        return 'other'

    def scrape_url(self, doc):
        return self._url

    def scrape_description(self, doc):
        tag = doc.html.head.findAll('meta', attrs={"name":"description"})
        result = "".join([t['content'] for t in tag])
        return result
    
    def scrape_price_amount(self, doc):
        tag = doc.html.body.select('span[class*=price]')
        conditions = ['span[class*=Price]', 'span[class*=Price]', 'div[class*=price]']

        for condition in conditions:
            if len(tag) > 0:
                break
            tag = doc.html.body.select(condition)

            self['price_currency'] = tag[0].text[-1:] if len(tag)>0 else "원"
        
        return tag[0].text[:-1] if len(tag)>0 else "알 수 없음"

    def scrape_price_currency(self, doc):
        return "원"