from bs4 import BeautifulSoup
import requests

#make class, load urls in here, make functions for updating etc.
def update_products(url):
    """
    Works for both malts, yeast and hops
    :param url:
    :return:
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    for product in soup.findAll(class_='product'):
        print(product.h4.text)
        print(product.h4.a['href'])
        print(product.find(class_='price--withTax').text)


if __name__ == '__main__':
    update_products('https://www.brewshop.co.nz/yeast/')