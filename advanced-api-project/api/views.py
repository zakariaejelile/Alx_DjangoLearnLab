
'''

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles GET (list all books) and POST (create a new book).

    Permissions:
      - Anyone can view the list
      - Only authenticated users can create new books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET (retrieve single book), PUT/PATCH (update), DELETE (remove a book)

    Permissions:
      - Anyone can view book details
      - Only authenticated users can edit or delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Only authenticated users can modify
'''
from rest_framework import generics, permissions, mixins
from .models import Book
from .serializers import BookSerializer


class BookListView(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    ListView:
    - Lists all books (GET)
    - Public access allowed
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read access to everyone

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookDetailView(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    """
    DetailView:
    - Retrieves a single book by ID (GET)
    - Public access allowed
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BookCreateView(mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
    CreateView:
    - Create a new book (POST)
    - Only authenticated users can create
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookUpdateView(mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    """
    UpdateView:
    - Update an existing book (PUT/PATCH)
    - Authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BookDeleteView(mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    DeleteView:
    - Delete a book (DELETE)
    - Authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



