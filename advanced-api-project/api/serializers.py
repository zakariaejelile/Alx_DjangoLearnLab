from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields.
    Also contains custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        
        fields = '__all__'  # serialize all model fields (id, title, publication_year, author)

    def validate_publication_year(self, value):
       
        current_year = datetime.date.today().year  #Ensures the year is not greater than the current year.
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.") 
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    books:
      - Uses BookSerializer to represent related Book objects.
      - 'many=True' because one author can have many books.
      - 'read_only=True' here for the simple case where books are shown on the author
         response but are not created/updated via the author serializer.
      - To allow nested writes, you'd implement create() and update() to handle 'books' field.
    """
    books = BookSerializer(many=True, read_only=True) # Serializes Author model and includes a nested representation of that author's books.

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
