from .views import *
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('category/<slug>', CategoryView.as_view(), name="category"),
    path('brand/<slug>', BrandView.as_view(), name="brands"),
    path('signup', signup, name='signup'),
    path('product-detail/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('reviews', reviews, name='product-review'),
    path('cart', CartView.as_view(), name='product-cart'),
    path('wishlist', wishlist, name='wishlist'),
    path('search', SearchView.as_view(), name='product-search'),
    path('addtocart/<slug>', Add_Cart.as_view(), name='add-to-cart'),
    path('delete-cart/<slug>', delete_cart, name='delete-cart'),
    path('decrease-quantity/<slug>', decrease_cart_quantity, name='decrease-quantity'),
    path('addtowishlist/<slug>',add_to_wishlist,name = 'add-to-wishlist'),
    path('delete-wishlist/<slug>',remove_from_wishlist,name = 'remove_wishlist'),
    path('checkout',checkout,name = 'checkout'),

]
