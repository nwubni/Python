'''
This Python program scrapes a website (http://books.toscrape.com) to check if a book title on a specific topic is in stock.
To achieve it, this program uses the Python library called BeautifulSoup for pulling data from HTML and XML files.
'''
import re
from unicodedata import category
import requests
from bs4 import BeautifulSoup


def in_stock(title, topic):
    URL = "http://books.toscrape.com/"
    page = requests.get(url=URL)
    soup = BeautifulSoup(page.content, "html.parser")

    category = extract_category(soup=soup, topic=topic.lower())

    if(category == None):
        return False

    URL += category
    page_num = 1

    page = requests.get(url=URL + 'index.html')
    soup = BeautifulSoup(page.content, "html.parser")

    while(("Not Found" not in soup.find('title').text)):
        if(has_title(soup=soup, title=title.lower())):
            return True

        page_num += 1
        page = requests.get(url=URL + 'page-' + str(page_num) + '.html')
        soup = BeautifulSoup(page.content, "html.parser")

    return False


def extract_category(soup, topic):
    for a in soup.find_all('a'):
        if a.text.strip().lower() == topic:
            return a['href'][:-10]

    return None


def has_title(soup, title):
    for a in soup.find_all('a'):
        book_title = str(a.get('title'))

        if book_title.strip().lower() == title:
            return True

    return False


# print(in_stock("While You Were Mine", "Historical Fiction"))
print(in_stock("Online Marketing for Busy Authors: A Step-By-Step guide", "Self help"))
# print(in_stock("The MooSEwood Cookbook: Recipes from Moosewood Restaurant, Ithaca, New York", "food and driNk"))
# print(in_stock("While You Were Mine", "Science"))
