from .views import *
from django.urls import path

urlpatterns = [
				path ('',HomeView.as_view(), name = "home"),
				path('category/<slug>',CategoryView.as_view(),name = "category"),
				path('brand/<slug>',BrandView.as_view(), name = "brands"),
			  	path('signup',signup,name = 'signup'),
			  	path('product-detail/<slug>',ProductDetailView.as_view(), name='product-detail'),
			  	path('reviews',reviews, name = 'product-review')

			  ]