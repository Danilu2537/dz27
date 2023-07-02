from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category, Selection
from ads.validators import check_is_False
from users.models import User
from users.serializers import LocationSerializer


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    is_published = serializers.BooleanField(validators=[check_is_False], required=False)

    class Meta:
        model = Ad
        fields = "__all__"


class AdListSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    locations = SerializerMethodField()

    def get_locations(self, obj):
        return obj.author.locations.values_list('name', flat=True) or None

    class Meta:
        model = Ad
        fields = ['name', 'price', 'category', 'locations']


class UserAdSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'locations']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    owner = SlugRelatedField(slug_field='username', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
