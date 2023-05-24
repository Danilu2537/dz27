import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(View):
    def get(self, request):
        return JsonResponse(
            [category.serialize()
             for category in Category.objects.all()],
            status=200, safe=False)

    def post(self, request):
        return JsonResponse(Category.objects.create(
            **json.loads(request.body)
        ).serialize(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(View):
    def get(self, request):
        return JsonResponse(
            [ad.serialize()
             for ad in Ad.objects.all()],
            status=200, safe=False)

    def post(self, request):
        return JsonResponse(Ad.objects.create(
            **json.loads(request.body)
        ).serialize(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            self.get_object().serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            self.get_object().serialize(),
            status=200)
