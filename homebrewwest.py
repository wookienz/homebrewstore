from bs4 import BeautifulSoup
import requests

#make class, load urls in here, make functions for updating etc.
def update_products(url):
    """
    works for malt, yeast
    :param url:
    :return:
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    for product in soup.findAll(class_='product'):
        print(product.a['href'])
        print(product.find(class_='price').text)
        print(product.find(class_='name').text)


if __name__ == '__main__':
    update_products('https://www.homebrewwest.co.nz/products/category/20/hops?pgNmbr=3&pgSize=25&isScrollChunk=true'
                    '&chunkNumber=4')
