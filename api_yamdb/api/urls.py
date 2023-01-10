from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_yamdb.api.views import ReviewViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')


url_v1 = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(url_v1)),
]
