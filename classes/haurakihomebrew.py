from bs4 import BeautifulSoup
import requests


class brewerscoop():
    """

    """

    def __init__(self):
        """

        :param self:
        :return:
        """
        self.BASE_URL = 'https://www.haurakihomebrew.co.nz'
        #self.imported_grain_url = '/category/160453'
        self.grain_url = '/collections/beer-crushed-to-order-malted-barley-milled'
        self.dried_yeast_url = '/collections/beer-dry-beer-yeast'
        self.liquid_yeast_url = '/beer-white-labs-liquid-yeast'
        self.nz_hops = '/collections/beer-nz-hops-cone-pellet'
        self.imported_hops = '/collections/beer-imported-hops'
        self.all_urls = [self.dried_yeast_url, self.grain_url, self.nz_hops, self.imported_hops]
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
        pagination = soup.find('div', {'class': 'pagination'})
        if pagination:
            links = pagination.findAll('a')
            for link in links:
                a.append(self.BASE_URL + link['href'])
            a.pop(-1)
            a.append(self.BASE_URL + '/collections/' + url.rpartition('/')[-1] + '?page=1')
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
        This method needs to be changed for each brew website
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, features="html.parser")
        product_details = []
        products = soup.findAll('div', {'class': 'grid-product__wrapper'})
        for product in products:
            item_name = product.find('span', {'class': 'grid-product__title'}).text
            item_url = product.a['href']
            item_price = product.find('span', {'class': 'grid-product__price'}).text # 'Regular price  $6.80'
            item_price = item_price.split('\n')[4].lstrip() # cant get text value of inner text of douible span element, split it out.
            if product.find(class_='grid-product__sold-out'):
                item_qty_avail = 0
            else:
                item_qty_avail = 1
            product_details.append((item_price, item_name, item_qty_avail, item_url))
        return product_details

    def _store(self, deets_array):
        """
        Store the details of the items
        :param deets-array: an array of tuples. Each tuple contains name, url, price and availability
        :type: list
        :return: None
        """
        for a in deets_array:
            for b in a:
                print(b)


if __name__ == '__main__':
    t = brewerscoop()
    t.update_products()

