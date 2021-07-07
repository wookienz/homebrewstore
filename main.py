import bs4.element
from bs4 import BeautifulSoup
import requests


def updateshoppingcategories(url):
    r = GetShopFrontPage(url)
    check_multiple_pages(r.text)
    #getshoppingcategories_BC(r.text)


def GetShopFrontPage(url):
    """
    Get the shop front page html. Do stuff with data later
    :param url: url of shop
    :return: html of front page of shop
    """
    r = requests.get(url)
    return r


def check_multiple_pages(html):
    """
    find if multiple pages in that category
    :param html: html of page to look for page numbers at the bottom
    :return:

    TODO: code this properly.
    """
    soup = BeautifulSoup(html, features="html.parser")
    pages = soup.find(class_='shoppingnav')
    for page in pages:
        getshoppingcategories_BC(soup)

    #for page in pages:
    #getshoppingcategories_BC(page)


def getshoppingcategories_BC(soup):
    """
    From the page in the url passed, get all categories than can be selected. This is dependant on which page is stared
    on. All use class cmsItemLI
    :param soup: html of shop front page
    :return:
    """
    #soup = BeautifulSoup(html, features="html.parser")
    categories = soup.findAll(class_='cmsItemLI')
    for row in categories:
        storeitem(row)
        # ITEM = <a href="/product/1717388"><img alt="Shepherd's Delight" border="0" src="/images-320x320/500232/pid1717388/IMG_3796.JPG"/></a>
        # <a href="/product/1717388">Shepherd's Delight</a>
        # print(row)


def storeitem(item):
    """

    :param item:
    :return:
    """
    item_title = item.find(class_='cmsTitle')
    item_name = item_title.text  # bs4.element.ResultSet
    item_url = (item_title.find('a')['href']) #/product/1717376
    item_price = item.find(class_='value').text  #<b class="value">4.70</b>
    if item.find(class_='outofstock'):
        item_qty_avail = 0
    else:
        item_qty_avail = item.find(class_='qtyTextField')['value'] #<input class="qtyTextField" name="b_qty" size="4" value="1"/>
    print(item_price, item_name, item_qty_avail)
    return


if __name__ == '__main__':
    updateshoppingcategories('https://www.brewerscoop.co.nz/category/159656')

