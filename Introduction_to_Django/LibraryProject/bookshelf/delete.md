# Delete Operation

```python
from bookshelf.models import Book
book.delete()
Book.objects.all()
# Output: (1, {'bookshelf.Book': 1})
# <QuerySet []>
