from rest_framework import viewsets
from . import models, serializers

# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
