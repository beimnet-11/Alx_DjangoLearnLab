from bookshelf.models import Book

book = Book.objects.get(publication_year=1984)
book.delete()

all_books = Book.objects.all()
print(all_books)

'''
<QuerySet []>
'''

