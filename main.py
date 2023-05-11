# importing libraries we need
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# specifying database file
db = "db.db"

# connection object
connection = sqlite3.connect(db)

# cursor object
cursor = connection.cursor()

# specifying user agent
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--headless")
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'
edge_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Edge(options=edge_options)
driver.set_window_size(1080, 800)

# Input book names
continue_input = True
search_book_name = []
book_ids = []
user_list = []
n = 0

while continue_input == True:
    search_book_name.append(input("Book: ").replace(" ", "+"))
    if n >= 4:
        more_books = input("Do you want to add more books?  :   ")
        if more_books == "No" or more_books == "no":
            continue_input = False

    n += 1

# time count starts
start_time = time.time()
total_start_time = time.time()

# Finds number in given string
def Find_number(string):
    try:
        number = re.search(r'\b\d+', string)
        return int(number.group())
    except Exception as e:
        print("Error while finding number")

# Takes book name as input and outputs book id
def Search_book(link):
    r = requests.get("https://www.goodreads.com/search?q="+link)
    soup = BeautifulSoup(r.content, 'html.parser')
    book_link = soup.find(class_="bookTitle")['href']
    book_id = str(Find_number(book_link))
    book_name = str(soup.find(class_="bookTitle").find("span").string)
    print(book_name)
    print(f"Goodreads book id: {book_id}")
    return int(book_id)

# Finds users that rated given books more than 3 and outputs their ids
def Good_ratings(book_ids):
    statement = f"SELECT book_id_csv FROM book_id_map WHERE book_id IN ({', '.join(str(x) for x in book_ids)})"
    cursor.execute(statement)
    tuples = cursor.fetchall()
    search_book_ids = [row[0] for row in tuples]

    statement = f"SELECT user_id FROM book_id WHERE book_id IN ({', '.join(str(x) for x in search_book_ids)}) AND rating > 3"
    cursor.execute(statement)
    tuples = cursor.fetchall()
    result = [row[0] for row in tuples]
    return result

# Searches for values in list that has been repeated more than given number of times
def Find_duplicates(lst, number):
    counter = Counter(lst)

    duplicates = [[value, count] for value, count in counter.items() if count >= number]

    return duplicates

# Takes list of users that gave ratings to more than required number of books good rating as an input and outputs book ids of books that this users gave good ratings
def Users_search(users):
    cursor.execute(f"SELECT book_id FROM user_id WHERE user_id IN ({', '.join(str(x) for x in users)}) AND rating > 3")
    tuples = cursor.fetchall()
    result = [row[0] for row in tuples]

    return result

# Finds books that more than one percent of chosen users gave good ratings
def Recomend_books(books):
    books_unsorted = Find_duplicates(books, int(0.01 * len(recomended_users)))
    recomendations = sorted(books_unsorted, key=lambda x: x[1], reverse=True)
    return recomendations

# Searches for goodreads book ids
def Find_book_id(book_ids):
    statement = f"SELECT book_id FROM book_id_map WHERE book_id_csv IN ({', '.join(str(x) for x in book_ids)})"
    cursor.execute(statement)
    tuples = cursor.fetchall()
    search_book_ids = [int(row[0]) for row in tuples]
    return search_book_ids

# Takes book id as an input and outputs book names
def Book_name(book_ids):
    try:
        recomend = []
        for id in book_ids:
            try:
                link = "https://www.goodreads.com/book/show/" + str(id)
                driver.get(link)
                driver.implicitly_wait(2)
                title = driver.find_element(By.CSS_SELECTOR, "h1.Text.Text__title1").text
                recomend.append([title, link])
            except Exception as e:
                print(f"Error occured while trying to find the page {id}")
        return recomend
    except Exception as e:
        print("Error while finding the name of the book")

# Adds users book ids to the list
for n in search_book_name:
    try:
        book_ids.append(Search_book(n))
    except Exception as e:
        print("Error")

time_after_goodreads = time.time()
total_time_after_goodreads = time_after_goodreads - start_time
print(f"Goodreads is searched, time taken: {total_time_after_goodreads}")
start_time = time.time()

# Searching for ratings
try:
    user_list.extend(Good_ratings(book_ids))
except Exception as e:
    "Error while searching for ratings"
print(f"Found users: {len(user_list)}")

time_after_good_ratings = time.time()
total_time_after_good_ratings = time_after_good_ratings - start_time
print(f"Book ids is searched, time taken: {total_time_after_good_ratings}")

# Determine minimum overlap needed
len_input = len(search_book_name)

if len_input < 5:
    min_overlap = 2
elif len_input == 5:
    min_overlap = 2
elif len_input < 10:
    min_overlap = int(len_input * 0.3)
elif len_input < 25:
    min_overlap = int(len_input * 0.2)
else:
    min_overlap = 5

start_time = time.time()

# Finding users with similar interests
recomended_books = []
recomended_users = Find_duplicates(user_list, min_overlap)
print(f"Length of recomended users list:{len(recomended_users)}")

time_after_recomended_users = time.time()
total_time_after_recomended_users = time_after_recomended_users - start_time
print(f"Recomended users are found, time taken: {total_time_after_recomended_users}")
start_time = time.time()

# Finding books that those users gave good ratings to
users = [i[0] for i in recomended_users]
books = Users_search(users)
print(f"Length of recomended books: {len(books)}")
#print(recomended_books)

time_after_recomended_books = time.time()
total_time_after_recomended_books = time_after_recomended_books - start_time
print(f"Books are found, time taken: {total_time_after_recomended_books}")

start_time = time.time()

# Giving final 100 recommendations
print("Final recommendations: ")
hundred_recommendations = []
recomendations = Recomend_books(books)
for i in range(0, 100):
    hundred_recommendations.append(recomendations[i][0])
goodreads_ids = Find_book_id(hundred_recommendations)

filtered_recommendations = [x for x in goodreads_ids if x not in book_ids]

recommend = Book_name(filtered_recommendations)
for i in recommend:
    print(i)



time_after_final_recomendations = time.time()
total_time_after_final_recomendations = time_after_final_recomendations - start_time
print(f"Recomended books are found, time taken: {total_time_after_final_recomendations}")

end_time = time.time()
total_end_time = end_time - total_start_time
print(f"Time taken overall: {total_end_time}")

driver.quit()
cursor.close()
connection.close()


