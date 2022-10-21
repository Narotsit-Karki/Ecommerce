from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here
from django.views.generic import View
from datetime import datetime

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user = request.user).count()
        wishlist_count = Wishlist.objects.filter(user = request.user).count()
    else:
        cart_count , wishlist_count  =  0 , 0
    return cart_count, wishlist_count

class BaseView(View):
    my_views = {}
    my_views['Categories'] = Category.objects.all()
    my_views['Brands'] = Brand.objects.all()
    my_views['Sales'] = Product.objects.filter(labels='sale')
    my_views['Hots'] = Product.objects.filter(labels='hot')
    my_views['Recents'] = Product.objects.filter(labels='new')

    Brands_Count = {}

    for brand in my_views['Brands']:
        products = Product.objects.filter(brand=brand)
        Brands_Count[brand.name] = products.count()

    my_views['Brands_Count'] = Brands_Count


# for Home View
class HomeView(BaseView):

    def get(self, request):
        self.my_views
        self.my_views['Sliders'] = Slider.objects.all()
        self.my_views['Ads'] = Ad.objects.all()
        self.my_views['FeedBacks'] = FeedBack.objects.all()
        self.my_views['Cart_Count'] , self.my_views['Wishlist_Count'] = get_cart_count(request)


        return render(request, 'index.html', self.my_views)


class CategoryView(BaseView):
    def get(self, request, slug):
        self.my_views
        ids = Category.objects.get(slug=slug).id
        self.my_views['Cat_Products'] = Product.objects.filter(category_id=ids)
        self.my_views['Cart_Count'] , self.my_views['Wishlist_Count'] = get_cart_count(request)

        return render(request, 'category.html', self.my_views)


class BrandView(BaseView):
    def get(self, request, slug):
        self.my_views
        ids = Brand.objects.get(slug=slug).id
        self.my_views['Brand_Products'] = Product.objects.filter(brand_id=ids)
        self.my_views['Cart_Items'] = Cart.objects.filter(user=request.user)
        self.my_views['Cart_Count'] , self.my_views['Wishlist_Count'] = get_cart_count(request)

        return render(request, 'brands.html', self.my_views)


# for individual producst

class ProductDetailView(BaseView):
    def calc_average_rating(self):
        if self.my_views['Reviews'].count() > 0:
            five_star = self.my_views['Reviews'].filter(rating=5).count()
            four_star = self.my_views['Reviews'].filter(rating=4).count()
            three_star = self.my_views['Reviews'].filter(rating=3).count()
            two_star = self.my_views['Reviews'].filter(rating=2).count()
            one_star = self.my_views['Reviews'].filter(rating=1).count()
            average_rating = int(
                (one_star + 2 * two_star + 3 * three_star + 4 * four_star + 5 * five_star) / self.my_views[
                    'Reviews'].count())
        else:
            average_rating = 0
        return average_rating

    def get(self, request, slug):
        self.my_views
        product = Product.objects.get(slug=slug)
        self.my_views['Related_Products'] = Product.objects.filter(sub_category=product.sub_category)
        self.my_views['single_product'] = product
        self.my_views['Reviews'] = Review.objects.filter(slug=slug)
        self.my_views['Cart_Count'], self.my_views['Wishlist_Count'] = get_cart_count(request)
        self.my_views['Avg_Rating'] = self.calc_average_rating()

        return render(request, 'product-detail.html', self.my_views)


def signup(request):
    if request.method == "POST":
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['c_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} Already Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, f'Email {email} Already Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Signed up Successfully ')
                return redirect("accounts/login")
        else:
            messages.error(request, 'Enter Same Password on Both Fields')

    return render(request, 'signup.html')


def reviews(request):
    if request.method == 'POST':
        user = request.user
        review = request.POST['review']
        rating = request.POST['rating']
        slug = request.POST['slug']
        review_data = Review.objects.create(
            user=user,
            slug=slug,
            review=review,
            rating=rating,
            date=datetime.now(),

        )
        review_data.save()
        return redirect(f'/product-detail/{slug}')


class SearchView(BaseView):
    # attributename__icontains

    def search_algorithm(self, query):
        keyword = set()

        if "," in query:
            for word in query.split(","):
                keyword.add(word.strip(" "))

        elif " " in query:
            for word in query.split(" "):
                keyword.add(word)
        else:
            keyword = {query}

        self.my_views['search_products'] = []

        for word in keyword:
            if len(word) > 1:
                if Product.objects.filter(description__icontains=word).exists():
                    products = Product.objects.filter(description__icontains=word)

                    for product in products:
                        self.my_views['search_products'].append(product)

    def get(self, request):
        self.my_views
        self.my_views['Cart_Count'], self.my_views['Wishlist_Count'] = get_cart_count(request)
        if request.method == "GET":

            query = request.GET['query']

            self.search_algorithm(query)

            if len(self.my_views['search_products']) == 0:
                messages.info(request, 'Search query not found')

                return redirect(request.META.get('HTTP_REFERER'))

        return render(request, 'product-search.html', self.my_views)


class Add_Cart(LoginRequiredMixin, BaseView):
    login_required = True

    def add_to_cart(self, user, price, item, slug):
        if not Cart.objects.filter(user=user, slug=slug).exists():
            quantity = 1
            total = price
            cart_object = Cart.objects.create(
                user=user,
                items=item,
                slug=item.slug,
                quantity=quantity,
                total=price,
                price=price,
                checkout=False
            )
            cart_object.save()
            # return true for new items  and false for previous this is used only to show messages on our template
            return True
        else:
            quantity = Cart.objects.get(user=user, slug=slug).quantity
            quantity += 1
            total = quantity * price
            Cart.objects.filter(slug=slug, user=user).update(quantity=quantity, total=total)
            return False

    def get(self, request, slug):
        if Product.objects.filter(slug=slug).exists():

            item = Product.objects.get(slug=slug)
            price = item.discount if item.discount > 0 else item.price

            if self.add_to_cart(request.user, price, item,slug):
                messages.success(request, f'{item.pname} added to your cart')
            else:
                messages.info(request, f'{item.pname} already added to your cart')

        else:
            messages.error(request, 'Selected Product Not Found')

        return redirect(request.META.get('HTTP_REFERER'))

    #


@login_required
def delete_cart(request, slug):
    if Cart.objects.filter(slug=slug, user=request.user).exists():
        Cart.objects.filter(slug=slug).delete()
        try:
            item_name = Product.objects.get(slug=slug).pname
        except:
            item_name = str()

        messages.success(request, f'{item_name} removed from the cart')

    return redirect(request.META.get('HTTP_REFERER'))


def decrease_cart_quantity(request, slug):
    if Cart.objects.filter(slug=slug, user=request.user).exists():
        cart = Cart.objects.get(slug=slug, user=request.user)
        quantity = cart.quantity
        if quantity > 1:
            quantity -= 1
            total = quantity * cart.price
            Cart.objects.filter(slug=slug, user=request.user).update(quantity=quantity, total=total)

    return redirect('/cart')



class CartView(LoginRequiredMixin,BaseView):
    def get(self, request):
        self.my_views
        self.my_views['Cart_Count'] , self.my_views['Wishlist_Count'] = get_cart_count(request)
        subtotal, shipping, grand_total = 0, 50, 0
        self.my_views['Shipping'] = shipping
        # total price calculate
        self.my_views['Cart_Items'] = Cart.objects.filter(user =request.user , checkout = False)
        for cart_item in self.my_views['Cart_Items']:
            subtotal += cart_item.total

        self.my_views['Sub_Total'] = subtotal
        self.my_views['Grand_Total'] = shipping + subtotal

        return render(request, 'cart.html', self.my_views)

def add_to_wishlist(request,slug):
    if Product.objects.filter(slug=slug).exists():
        item = Product.objects.get(slug=slug)
        if not Wishlist.objects.filter(slug = slug,user = request.user).exists():

            price = item.discount if item.discount > 0 else item.price
            wishlist_object = Wishlist.objects.create(
                items = item,
                user = request.user,
                price = price,
                slug = slug
            )
            wishlist_object.save()
            messages.success(request, f'{item.pname} added to your wishlist')

        else:
            messages.info(request, f'{item.pname} already added to your wishlist')

    else:
        messages.error(request, 'Selected Product Not Found')

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_from_wishlist(request,slug):
    if Wishlist.objects.filter(slug = slug, user=request.user).exists():
        Wishlist.objects.filter(slug = slug).delete()
        try:
            item_name = Product.objects.get(slug=slug).pname
        except:
            item_name = str()

        messages.success(request, f'{item_name} removed from the wishlist')

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist(request):
    view = {}
    view['WishLists'] = Wishlist.objects.filter(user=request.user)
    view['Cart_Count'], view['Wishlist_Count'] = get_cart_count(request)

    return render(request , 'wishlist.html',view)

@login_required
def checkout(request):

    return render(request,'checkout.html')



# --------------API VIEWS -------------#
from .serializers import *
from rest_framework import viewsets
import django_filters.rest_framework
from rest_framework import generics , filters

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# django-export-import

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filterset_fields= ['category','sub_category','brand','stock','labels']
    search_fields = ['pname','description','specification']
    ordering_fields = ['price','id','name']
    #django_filter for ascending descending and different filters

class ProductDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductSerializer(snippet)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # put function to update data
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductSerializer(snippet, data=request.data, partial=True)
        # partial = True then we can update only one field in the models also if partial = False we need to update all  the fields in productserializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)