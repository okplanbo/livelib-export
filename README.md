# LiveLib CSV Book Exporter / Backup

This script is designed to scrape book data from the LiveLib.ru website, focusing on books that a user has read, wishes to read, or is currently reading. The data includes the title, ISBN, rating, and URL of each book.

## Requirements

Python 3.x is required to run this script. All dependencies can be installed using:

```pip install -r requirements.txt```

## Usage

Please replace USER_ID with your actual LiveLib user ID in the script before using it to correctly scrape your data.

To run the script, simply execute:

```python main.py```

Ensure you have the appropriate user permissions and internet connection to access the LiveLib website.

## Features

- Extracts book lists for different shelves: Read, Wish List, and Currently Reading.
- Saves the complete list of books with details into a CSV file `livelib-export.csv`.

## Disclaimer

This script is for personal use only. Use it responsibly and respect the website's terms of service.
