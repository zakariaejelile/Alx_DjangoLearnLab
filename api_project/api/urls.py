from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns = [
    # Optional ListAPIView route
    path('books/', BookList.as_view(), name='book-list'),

    # Router CRUD routes
    path('', include(router.urls)),

    # Token endpoint (POST: username, password)
    path('get-token/', obtain_auth_token, name='get-token'),
]


