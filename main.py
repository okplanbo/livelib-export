from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument('--incognito')
options.add_argument('--disable-plugins-discovery')
options.add_argument('--start-maximized')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

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
    driver.get(url)
    time.sleep(3)
    if (current_page):
        print('getting page %s' % current_page)
    # print('status code %s' % driver.page_source.status_code)
    return BeautifulSoup(driver.page_source, 'html.parser')


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
                book["rating"] = round(float(rating_value)) if rating_value else None
            result_dict_list.append(book)

        has_more = bool(soup.find("div", class_="pagination-more-left"))

        if (has_more):
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


def get_book_info(book_list):
    for book in book_list:
        soup = get_page(DOMAIN + book['url'], None)
        isbn = soup.find("meta", property="book:isbn")
        title = soup.find("meta", property="og:title")
        book['isbn'] = isbn["content"].replace("-", "") if isbn else None
        book['title'] = title["content"] if title else None


print('getting ISBN and book titles, please wait')
get_book_info(read_books)
get_book_info(wish_books)
get_book_info(reading_books)

# Let's compile the final book list out of 3 lists. We will add shelves
# for 'Goodreads' as categories in process

fieldnames = ['title', 'isbn', 'rating', 'url', 'shelves']
final_list = []

for book in read_books:
    book["shelves"] = "read"
    final_list.append(book)

for book in wish_books:
    book["shelves"] = "to-read"
    final_list.append(book)

for book in reading_books:
    book["shelves"] = "currently-reading"
    final_list.append(book)

# And finally save everything to csv file

with open('livelib-export.csv', 'w', newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(final_list)

print('All done!')
