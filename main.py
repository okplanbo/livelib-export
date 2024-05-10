import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://www.livelib.ru/reader/'
USER_ID = ''
READ_URL = '/read'
WISH_URL = '/wish'
READING_URL = '/reading'
BOOK_BASE = 'https://www.livelib.ru/book/'
APPENDIX = '/listview/smalllist/~'

current_page = 1

read_books = []
wish_book_ids = []
reading_book_ids = []

has_more = True


def get_page(url):
    page = requests.get(url)
    print('getting page %s' % current_page)
    print('status code %s' % page.status_code)
    return BeautifulSoup(page.text, 'html.parser')


while (has_more):
    read_page_url = BASE_URL + USER_ID + READ_URL + APPENDIX + str(current_page)
    soup = get_page(read_page_url)
    booklist = soup.find("div", {"id": "booklist"}).find_all("div", class_="book-item-manage")  # noqa: E501

    for book_container in booklist:
        book = {}
        book["url"] = book_container.find("a", class_="brow-book-name with-cycle")['href']  # noqa: E501
        book["rating"] = book_container.find("span", class_="brow-rating marg-right").find("span", class_="rating-value").text  # noqa: E501
        read_books.append(book)

    has_more = bool(soup.find("div", class_="pagination-more-left"))

    if (has_more):
        time.sleep(2)
        current_page += 1

for book in read_books:
    print(book["url"])
