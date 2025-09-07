from .models import Author, Library, Librarian, Book

# All books by a specific Author
author_name = 'Elyas'
author = Author.objects.get(name=author_name)
all_book_by_author = Book.objects.filter(author=author)

# All books in a library
library_name = 'Central'
library = Library.objects.get(name=library_name)
all_books_in_library = library.books.all()

# Retrieve a librarian for a library
librarian = Librarian.objects.get(library=library)