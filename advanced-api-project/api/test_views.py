from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITest(APITestCase):

    def setUp(self):
        # Create test user for authenticated requests
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # Create test author and books
        self.author = Author.objects.create(name="John Doe")
        self.book1 = Book.objects.create(title="Python Basics", publication_year=2022, author=self.author)
        self.book2 = Book.objects.create(title="Advanced Python", publication_year=2023, author=self.author)

        # URLs
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        self.update_url = reverse("book-update", kwargs={"pk": self.book1.pk})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book2.pk})

    # GET LIST
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    # CREATE (Auth Required)
    def test_create_book_requires_auth(self):
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "API Testing", "publication_year": 2024, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # UPDATE (Auth Required)
    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "Updated Title", "publication_year": 2023, "author": self.author.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # DELETE (Auth Required)
    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ❇ Filtering
    def test_filter_books_by_year(self):
        response = self.client.get(self.list_url + "?publication_year=2022")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    #  Searching
    def test_search_books(self):
        response = self.client.get(self.list_url + "?search=Advanced")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Advanced Python")

    #  Ordering
    def test_order_books_by_title_desc(self):
        response = self.client.get(self.list_url + "?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
