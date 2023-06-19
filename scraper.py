from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re


# specifying user agent
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--headless")
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'
edge_options.add_argument(f'user-agent={user_agent}')
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(options=edge_options)
driver.set_window_size(1080, 800)

# Finds number in given string
def number_in_string(string):
    try:
        number = re.search(r'\b\d+', string)
        return int(number.group())
    except Exception as e:
        print("Error while finding number")

# Takes book name as input and outputs book id
def find_goodreads_book_id(link):
    r = requests.get("https://www.goodreads.com/search?q="+link)
    soup = BeautifulSoup(r.content, 'html.parser')
    book_titles = soup.find_all(class_="bookTitle")
    book_info = []
    for item in book_titles:
        link = item["href"]
        book_item = []
        book_item.append(number_in_string(link))
        book_item.append(str(item.find("span").string))
        book_info.append(book_item)

    return book_info

# Takes book id as an input and outputs book names and links to Goodreads
def find_book_name(book_ids):
    print("Searching for books names...")
    try:
        recommend = []
        for id in book_ids:
            try:
                link = "https://www.goodreads.com/book/show/" + str(id)
                driver.get(link)
                driver.implicitly_wait(1)
                title = driver.find_element(By.CSS_SELECTOR, "h1.Text.Text__title1").text
                recommend.append([title, link])
                print(recommend[len(recommend)-1])
            except Exception as e:
                print(f"Error occured while trying to find the page {id}")
        driver.quit()
        return recommend
    except Exception as e:
        print("Error while finding the name of the book")
