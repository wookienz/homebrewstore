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
    #print(r.text)
    soup = BeautifulSoup(r.text, features="html.parser")
    for product in soup.findAll(class_='product-image'):
        print(product.find(class_='price').text)
        print(product.a['href'])
        print(product.find(class_='product-name').a)



if __name__ == '__main__':
    update_products('https://leagueofbrewers.co.nz/homebrew-beer-supplies/beer-brewing-ingredients/malt-for-making-beer/grain-for-brewing')
