from bs4 import BeautifulSoup
import requests

import os
from selenium import webdriver
import time


class brewerscoop():
    """

    """

    def __init__(self):
        """

        :param self:
        :return:
        """
        self.BASE_URL = 'https://www.brewerscoop.co.nz'
        self.imported_grain_url = '/category/160453'
        self.nz_grain_url = '/category/160451'
        self.dried_yeast_url = '/category/146269'
        self.liquid_yeast_url = '/category/146268'
        self.nz_hops = '/category/159655'
        self.imported_hops = '/category/159656'
        #yeasts category / 159689, /category/159691, /category/159690
        self.all_urls = [self.dried_yeast_url, self.nz_grain_url, self.nz_grain_url,
                         self.imported_grain_url, self.nz_hops, self.imported_hops]
        self.s = requests.session()
        return

    def update_products(self):
        """
        go through all types of products and update the database
        :return:
        """
        for product_url in self.all_urls:
            products = self._update_single_product(self.BASE_URL + product_url)
            #entire_page = self.load_entire_page(self.BASE_URL + product_url)
            #details = self._update_single_product(entire_page)
            self._store(products)
        return

    def _combine_yeast_pages(self, url):
        """
        Return urls containing the tow yeast pages. Both dried and liquid.
        :return:
        """
        html = self._parseurl(url)
        soup = BeautifulSoup(html.text, features="html.parser")
        elements = soup.findAll('li', {'class': 'cmsItemLI'})
        return

    def load_entire_page(self, url):
        """
        Use selenium driver to load chrome, scroll then pass resultant html.
        NOT REQUIRED FOR THIS SITE
        :return:
        """
        html = self._parseurl(url)
        return html.text

    def _parseurl(self, url, sub='get', payload=''):
        if sub == 'get':
            r = self.s.get(url, verify=False)
        else:
            r = self.s.post(url, data=payload, verify=False)
        return r

    def _find_more_pages(self, url):
        """
        Parse html file and figure out the links to the next page
        :return: the return variable is a list of "next links"
       """
        html = self._parseurl(url)
        soup = BeautifulSoup(html.text, features="html.parser")
        a = []
        if soup.find('p', {'class': 'shoppingnav'}):
            links = soup.findAll('a', {'class': 'pagenav'})
            for link in links:
                a.append(self.BASE_URL + link['href'])
        a.append(self.BASE_URL + '/category/' + url.rpartition('/')[-1] + '?nav=shoppingnav&page_start=0')  # adds current page to the list
        return a

    def _update_single_product(self, url):
        """
        works for malt, yeast and hops. doest load the whole page however, need to work out how to JS loading whole page

        :param url:
        :type url:
        :return:
        """
        products = []
        all_products = []
        more_pages = self._find_more_pages(url)
        for page in more_pages:
            html = self.load_entire_page(page)
            products = self._extract_products_from_page(html)
            all_products = all_products + products
        return all_products

    def _extract_products_from_page(self, html):
        """

        :param html:
        :return:
        """
        soup = BeautifulSoup(html, features="html.parser")
        product_details = []
        products = soup.findAll('li', {'class': 'cmsItemLI'})
        for product in products:
            item_name = product.find(class_='cmsTitle').a.text
            item_url = product.find(class_='cmsTitle').a['href']  # /product/1717376
            item_price = product.find(class_='value').text  # <b class="value">4.70</b>
            if product.find(class_='outofstock'):
                item_qty_avail = 0
            else:
                item_qty_avail = product.find(class_='qtyTextField')[
                    'value']  # <input class="qtyTextField" name="b_qty" size="4" value="1"/>
            product_details.append((item_price, item_name, item_qty_avail, item_url))
        return product_details

    def _store(self, deets_array):
        """
        Store the details of the items
        :return:
        """
        for a in deets_array:
            for b in a:
                print(b)


if __name__ == '__main__':
    t = brewerscoop()
    t.update_products()

