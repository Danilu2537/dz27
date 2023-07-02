from rest_framework.routers import SimpleRouter

from ads.views.cat import CategoryViewSet

router = SimpleRouter()
router.register('', CategoryViewSet, basename='category')
urlpatterns = router.urls
