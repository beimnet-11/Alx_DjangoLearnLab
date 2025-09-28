from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return f'{self.author}, {self.title}'