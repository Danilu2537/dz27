import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    queryset = Category.objects.order_by("name")
    fields = ['name']

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            [category.serialize()
             for category in self.get_queryset()],
            status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category
    field = ['name']

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            self.get_object().serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    success_url = '/'

    def post(self, request, *args, **kwargs):
        return JsonResponse(Category.objects.create(
            **json.loads(request.body)
        ).serialize(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)
        if 'name' in cat_data:
            self.object.name = cat_data['name']

        self.object.save()

        return JsonResponse(
            self.object.serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse(
            {"status": "ok"},
            status=200)
