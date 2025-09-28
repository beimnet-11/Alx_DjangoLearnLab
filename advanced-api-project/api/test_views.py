from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book
from django.contrib.auth.models import User

class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")  

        
        self.book = Book.objects.create(title="Django Basics", author="John Doe", publication_year=2024)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Django Basics", str(response.data))

    def test_create_book(self):
        url = reverse('book-list')
        data = {"title": "New Book", "author": "Jane Doe", "publication_year": 2025}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {"title": "Updated Title", "author": "John Doe", "publication_year": 2024}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_filter_books_by_year(self):
        url = reverse('book-list') + "?publication_year=2024"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(book['title'] == "Django Basics" for book in response.data))

    def test_search_books_by_title(self):
        url = reverse('book-list') + "?search=Django"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Django" in book['title'] for book in response.data))

    def test_order_books_by_title(self):
        Book.objects.create(title="AAA Book", author="Someone", publication_year=2023)
        url = reverse('book-list') + "?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

