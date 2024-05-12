import requests
from bs4 import BeautifulSoup
import time

DOMAIN = 'https://www.livelib.ru'
BASE_USER_URL = DOMAIN + '/reader/'
USER_ID = ''
READ_URL = '/read'
WISH_URL = '/wish'
READING_URL = '/reading'
BOOK_BASE = 'https://www.livelib.ru/book/'
APPENDIX = '/listview/smalllist/~'

read_books = []
wish_books = []
reading_books = []

def get_page(url, current_page):
    page = requests.get(url)
    if (current_page):
        print('getting page %s' % current_page)
    print('status code %s' % page.status_code)
    return BeautifulSoup(page.text, 'html.parser')


def get_book_list(page_type):
    result_dict_list = []
    has_more = True
    current_page = 1

    while (has_more):
        read_page_url = BASE_USER_URL + USER_ID + page_type + APPENDIX + str(current_page)  # noqa: E501
        soup = get_page(read_page_url, current_page)
        booklist = soup.find("div", {"id": "booklist"}).find_all("div", class_="book-item-manage")  # noqa: E501

        for book_container in booklist:
            book = {}
            book["url"] = book_container.find("a", class_="brow-book-name with-cycle")['href']  # noqa: E501
            rating_span = book_container.find("span", class_="brow-rating marg-right")  # noqa: E501
            if (rating_span):
                rating_value = rating_span.find("span", class_="rating-value").text  # noqa: E501
                book["rating"] = rating_value
            result_dict_list.append(book)

        has_more = bool(soup.find("div", class_="pagination-more-left"))

        if (has_more):
            time.sleep(2)
            current_page += 1

    return result_dict_list


# First let's get book lists

read_books = get_book_list(READ_URL)

print('read books: %s' % len(read_books))
print('')

wish_books = get_book_list(WISH_URL)

print('wishlist count: %s' % len(wish_books))
print('')

reading_books = get_book_list(READING_URL)

print('reading now: %s' % len(reading_books))
print('')

# Then add ISBN and book titles from book info pages

