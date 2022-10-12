from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here
from django.views.generic import View
from datetime import datetime

class BaseView(View):
	my_views =  {}
	my_views['Categories'] = Category.objects.all()
	my_views['Brands'] = Brand.objects.all()
	my_views['Sales'] = Product.objects.filter(labels = 'sale')
	my_views['Hots'] = Product.objects.filter(labels = 'hot')
	my_views['Recents'] = Product.objects.filter(labels = 'new')
	Brands_Count = {}
	
	for brand in my_views['Brands']:
			products = Product.objects.filter(brand = brand)
			Brands_Count[brand.name] = products.count()
			
	my_views['Brands_Count'] = Brands_Count
	


# for Home View	
class HomeView(BaseView):

	def get(self,request):
		self.my_views
		self.my_views['Sliders'] = Slider.objects.all()
		self.my_views['Ads'] = Ad.objects.all()
		self.my_views['FeedBacks'] = FeedBack.objects.all()
		
		
		return render(request,'index.html',self.my_views)
		



	
class CategoryView(BaseView):
	def get(self,request,slug):
		self.my_views
		ids = Category.objects.get(slug = slug).id
		self.my_views['Cat_Products'] = Product.objects.filter(category_id = ids)
		return render(request,'category.html',self.my_views)

class BrandView(BaseView):
	def get(self,request,slug):
		self.my_views
		ids = Brand.objects.get(slug = slug).id
		self.my_views['Brand_Products'] = Product.objects.filter(brand_id = ids)
		return render(request , 'brands.html',self.my_views)
# for individual producst

class ProductDetailView(BaseView):
	def get(self,request,slug):
		self.my_views
		product  = Product.objects.get(slug = slug)
		self.my_views['Related_Products'] = Product.objects.filter(sub_category = product.sub_category)
		self.my_views['single_product'] = product
		self.my_views['Reviews'] = Review.objects.filter(slug = slug)
		if self.my_views['Reviews'].count() > 0:
			five_star = self.my_views['Reviews'].filter(rating = 5).count()
			four_star = self.my_views['Reviews'].filter(rating = 4).count()
			three_star = self.my_views['Reviews'].filter(rating = 3).count()
			two_star = self.my_views['Reviews'].filter(rating = 2).count()
			one_star = self.my_views['Reviews'].filter(rating = 1).count()
			average_rating = int((one_star + 2 * two_star + 3 * three_star + 4 * four_star + 5 * five_star)/self.my_views['Reviews'].count())
		else:
			average_rating = 0
		self.my_views['Avg_Rating'] = average_rating
		return render(request,'product-detail.html',self.my_views)


def signup(request):

	if request.method == "POST":
		username = request.POST['uname']
		email = request.POST['email']
		password = request.POST['password']
		confirm_password = request.POST['c_password']
		if password == confirm_password:
			if User.objects.filter(username = username).exists():
				messages.error(request,'Username Already Taken')
				return redirect('signup')
			elif User.objects.filter(email = email).exists():
				messages.error(request,'Email Already Taken')
				return redirect('signup')
			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password
					)
				user.save()
				messages.success(request,'Signed up Successfully ')
				return redirect("/")
		else:
			messages.error(request,'Enter Same Password on Both Fields')

	return render(request,'signup.html')


def reviews(request):
	if request.method == 'POST':
		user = request.user
		review = request.POST['review']
		rating = request.POST['rating']
		slug = request.POST['slug']
		review_data = Review.objects.create(
			user = user,
			slug = slug,
			review =  review,
			rating = rating,
			date = datetime.now(),

			)
		review_data.save()
		return redirect(f'/product-detail/{slug}')