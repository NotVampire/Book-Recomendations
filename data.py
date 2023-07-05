import sqlite3
from collections import Counter

# specifying database file
db = f'./data/db.db'

# connection object
connection = sqlite3.connect(db)

# cursor object
cursor = connection.cursor()

# Finds users that rated given books more than 3 and outputs their ids
def good_rating_users(book_ids):
    statement = f"SELECT user_id FROM goodreads WHERE book_id IN ({', '.join(str(x) for x in book_ids)})"
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

# Creating a temporary table for the users and joining it with the book_id table
def create_user_temp_table(users):
    cursor.execute("CREATE TEMPORARY TABLE temp_user(user_id INTEGER PRIMARY KEY)")
    cursor.executemany("INSERT INTO temp_user(user_id) VALUES (?)", [(user,) for user in users])
    cursor.execute("CREATE INDEX idx_user_id_temp ON temp_user (user_id);")
    connection.commit()

# Takes list of users that gave ratings to more than required number of books good rating as an input and outputs book ids of books that this users gave good ratings
def find_books_from_users():
    print("Searching for books that these users have given good ratings to...")
    cursor.execute("""
    SELECT book_id 
    FROM goodreads
    INNER JOIN temp_user 
    ON goodreads.user_id = temp_user.user_id 
    """)
    tuples = cursor.fetchall()
    result = [row[0] for row in tuples]
    cursor.execute("DROP TABLE temp_user")
    return result

# Finds books that more than one percent of chosen users gave good ratings and sorts the list
def find_recommended_books(books, recomended_users):
    books_unsorted = find_duplicates(books, int(0.01 * len(recomended_users)))
    recommendations = sorted(books_unsorted, key=lambda x: x[1], reverse=True)
    return recommendations

# Searches for goodreads book ids

