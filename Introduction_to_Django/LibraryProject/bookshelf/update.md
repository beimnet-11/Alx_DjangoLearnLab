update_book = Book.objects.get(title='1984')
update_book.title = "Nineteen Eighty-Four"
update_book.save()

'''
Nineteen Eighty-Four
'''