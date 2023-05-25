import scraper
import data
from timer import Program, Timer
import input_output

# Collect books names from user
goodreads_book_ids = input_output.collect_books_names()

# time count starts
total = Program()
timer = Timer()
total.start_timer()


# Searching for users that have given rating of 4 or 5 to books the user provided
timer.start_timer()
user_list = []
try:
    user_list.extend(data.good_rating_users(goodreads_book_ids))
except Exception as e:
    "Error while searching for ratings"
print(f"Found users: {len(user_list)}")
timer.finish_timer("Users that gave good rating to at least one book from the list are found")


# Determine minimum overlap for users to make it into the list
timer.start_timer()
min_overlap = data.determine_overlap(goodreads_book_ids)

# Finding users that have given good ratings to more than 1 book from the list
recomended_books = []
recomended_users = data.find_duplicates(user_list, min_overlap)
timer.finish_timer("Users with similar interests are found")


# Finding books that these users gave good ratings to
timer.start_timer()
users = [i[0] for i in recomended_users]
books = data.find_books_from_users(users)
print(f"Length of recomended books: {len(books)}")
timer.finish_timer("Books that these users gave good ratings to are found")


# Giving final 100 recommendations
timer.start_timer()
hundred_recommendations = []
recommendations = data.find_recommended_books(books, recomended_users)
for i in range(0, 100):
    hundred_recommendations.append(recommendations[i][0])
goodreads_ids = data.find_goodreads_book_id(hundred_recommendations)
filtered_recommendations = [x for x in goodreads_ids if x not in goodreads_book_ids]
print("Final recommendations: ")
recommend = scraper.find_book_name(filtered_recommendations)
timer.finish_timer("Recommended books are found")

# Time taken overall
total.finish_timer()
