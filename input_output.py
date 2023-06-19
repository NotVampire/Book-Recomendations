import scraper

def collect_books_names():
    book_ids = []
    n = 0

    while True:
        book_name = input("Book: ").replace(" ", "+")
        book_info = scraper.find_goodreads_book_id(book_name)
        for i in book_info:
            print(i[1])
            right_book = input("Is this the book? ")
            if right_book in ["Yes", "yes", "y"]:
                book_ids.append(i[0])
                break
        if n >= 4:
            more_books = input("Do you want to add more books?  :   ")
            if more_books in ["No", "no", "n"]:
                break
        n += 1

    return book_ids