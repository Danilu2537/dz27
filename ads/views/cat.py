from rest_framework.viewsets import ModelViewSet

from ads.models import Category
from ads.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
