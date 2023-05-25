import scraper

def collect_books_names():
    continue_input = True
    book_ids = []
    n = 0

    while continue_input == True:
        book_name = input("Book: ").replace(" ", "+")
        book_info = scraper.find_goodreads_book_id(book_name)
        for i in book_info:
            print(i[1])
            right_book = input("Is this the book? ")
            if right_book == "yes" or right_book == "Yes":
                book_ids.append(i[0])
                break
        if n >= 4:
            more_books = input("Do you want to add more books?  :   ")
            if more_books == "No" or more_books == "no":
                continue_input = False
        n += 1

    return book_ids