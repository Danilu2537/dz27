from django.http import JsonResponse

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdSerializer, AdListSerializer, AdDetailSerializer, AdCreateSerializer


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by('-price')
    serializers = {
        "list": AdListSerializer,
        "retrieve": AdDetailSerializer,
        "create": AdCreateSerializer,
    }
    default_serializer = AdSerializer
    permissions = {
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsOwner | IsStaff],
        "destroy": [IsOwner | IsStaff],
        "partial_update": [IsOwner | IsStaff],
    }
    default_permissions = [AllowAny]

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permissions)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category__id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get('price_from')
        if price_from and price_from.isdigit():
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to and price_to.isdigit():
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get('image')
        self.object.save()

        return JsonResponse(self.object.serialize(), status=200)
