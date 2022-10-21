# Routers provide an easy way of automatically determining the URL conf.
from django.urls import include , path
from rest_framework import routers
from .views import ProductViewSet, ProductListView , ProductDetail

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
# list api is not registered in router only models api

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('product-filter/',ProductListView.as_view(),name = 'api-filter'),
    # /', SnippetList.as_view()),
    path('product-crud/<int:pk>/', ProductDetail.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]