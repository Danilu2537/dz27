import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location

TOTAL_ON_PAGE = 10


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.prefetch_related("locations")\
        .annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))\
        .order_by("username")
    fields = "__all__"

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        users_on_page = paginator.get_page(page_number)

        return JsonResponse({"items": [user.serialize() | {"total_ads": user.total_ads}
                                       for user in users_on_page],
                             "total": paginator.count,
                             "num_pages": paginator.num_pages, },
                            status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User
    fields = "__all__"

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            self.object.serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = "__all__"
    success_url = '/'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        locations = user_data.pop('locations')
        user = User.objects.create(**user_data)
        for location in locations:
            loc, _ = Location.objects.get_or_create(name=location)
            user.locations.add(loc)

        if 'author' in user_data:
            user_data['author'] = get_object_or_404(User, pk=user_data['author'])

        return JsonResponse(User.objects.create(
            **user_data
        ).serialize(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        if "locations" in user_data:
            locations = user_data.get('locations')
            self.object.locations.clear()
            for location in locations:
                loc, _ = Location.objects.get_or_create(name=location)
                self.object.locations.add(loc)
        if "first_name" in user_data:
            self.object.first_name = user_data['first_name']
        if "last_name" in user_data:
            self.object.last_name = user_data['last_name']
        if "username" in user_data:
            self.object.username = user_data['username']
        if "password" in user_data:
            self.object.password = user_data['password']
        if "age" in user_data:
            self.object.age = user_data['age']

        self.object.save()

        return JsonResponse(
            self.object.serialize(),
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    fields = "__all__"

    def delete(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.delete()

        return JsonResponse({"status": "ok"},
                            status=200)
