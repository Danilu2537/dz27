import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from users.models import User

TOTAL_ON_PAGE = 10


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    queryset = Ad.objects.order_by("-price")
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        ads_on_page = paginator.get_page(page_number)

        return JsonResponse({"items": [ad.serialize()
                                       for ad in ads_on_page],
                             "total": paginator.count,
                             "num_pages": paginator.num_pages, },
                            status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            self.object.serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']
    success_url = '/'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if 'author' in ad_data:
            ad_data['author'] = get_object_or_404(User, pk=ad_data['author'])
        if 'category' in ad_data:
            ad_data['category'] = get_object_or_404(Category, pk=ad_data['category'])

        return JsonResponse(Ad.objects.create(
            **ad_data
        ).serialize(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        if 'name' in ad_data:
            self.object.name = ad_data['name']
        if 'author' in ad_data:
            self.object.author = get_object_or_404(User, pk=ad_data['author'])
        if 'description' in ad_data:
            self.object.description = ad_data['description']
        if 'price' in ad_data:
            self.object.price = ad_data['price']
        if 'is_published' in ad_data:
            self.object.is_published = ad_data['is_published']
        if 'category' in ad_data:
            self.object.category = get_object_or_404(Category, name=ad_data['category'])

        self.object.save()

        return JsonResponse(
            self.object.serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']

    def delete(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.delete()

        return JsonResponse({"status": "ok"},
                            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'description', 'price', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get('image')
        self.object.save()

        return JsonResponse(self.object.serialize(), status=200)
