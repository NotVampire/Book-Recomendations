import sqlite3
from collections import Counter

# specifying database file
db = "db.db"

# connection object
connection = sqlite3.connect(db)

# cursor object
cursor = connection.cursor()

# Finds users that rated given books more than 3 and outputs their ids
def good_rating_users(book_ids):
    print("Searching for users that gave good ratings to books from the list...")
    statement = f"SELECT book_id_csv FROM book_id_map WHERE book_id IN ({', '.join(str(x) for x in book_ids)})"
    cursor.execute(statement)
    tuples = cursor.fetchall()
    search_book_ids = [row[0] for row in tuples]

    statement = f"SELECT user_id FROM book_id WHERE book_id IN ({', '.join(str(x) for x in search_book_ids)}) AND rating > 3"
    cursor.execute(statement)
    tuples = cursor.fetchall()
    result = [row[0] for row in tuples]
    return result

def determine_overlap(number_list):
    len_input = len(number_list)

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

    return min_overlap
# Searches for values in list that has been repeated more than given number of times
def find_duplicates(lst, number):
    counter = Counter(lst)
    duplicates = [[value, count] for value, count in counter.items() if count >= number]

    return duplicates

# Takes list of users that gave ratings to more than required number of books good rating as an input and outputs book ids of books that this users gave good ratings
def find_books_from_users(users):
    print("Searching for books that these users have given good ratings to...")
    cursor.execute(f"SELECT book_id FROM user_id WHERE user_id IN ({', '.join(str(x) for x in users)}) AND rating > 3")
    tuples = cursor.fetchall()
    result = [row[0] for row in tuples]

    return result

# Finds books that more than one percent of chosen users gave good ratings and sorts the list
def find_recommended_books(books, recomended_users):
    books_unsorted = find_duplicates(books, int(0.01 * len(recomended_users)))
    recomendations = sorted(books_unsorted, key=lambda x: x[1], reverse=True)
    return recomendations

# Searches for goodreads book ids
def find_goodreads_book_id(book_ids):
    statement = f"SELECT book_id FROM book_id_map WHERE book_id_csv IN ({', '.join(str(x) for x in book_ids)})"
    cursor.execute(statement)
    tuples = cursor.fetchall()
    search_book_ids = [int(row[0]) for row in tuples]
    cursor.close()
    connection.close()
    return search_book_ids
