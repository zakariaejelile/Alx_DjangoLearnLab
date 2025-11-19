from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList  # if you still use BookList

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns = [
    # Optional ListAPIView route
    path('books/', BookList.as_view(), name='book-list'),

    # Router CRUD routes
    path('', include(router.urls)),
]
