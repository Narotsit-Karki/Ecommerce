from django.shortcuts import render
from .models import *

# Create your views here
from django.views.generic import View

class BaseView(View):
	my_views = {}
	my_views['Categories'] = Category.objects.all()
	my_views['Brands'] = Brand.objects.all()



# for Home View	
class HomeView(BaseView):

	def get(self,request):
		rating = []
		self.my_views['Sliders'] = Slider.objects.all()
		self.my_views['Ads'] = Ad.objects.all()
		self.my_views['Hots'] = Product.objects.filter(labels = 'hot')
		self.my_views['Recents'] = Product.objects.filter(labels = 'new')
		self.my_views['FeedBacks'] = FeedBack.objects.all()
		for feedback in self.my_views['FeedBacks']:
			feedback.rating = range(feedback.rating)   
		return render(request,'index.html',self.my_views)
		


	
class CategoryView(BaseView):
	def get(self,request,slug):
		ids = Category.objects.get(slug = slug).id
		self.my_views['Cat_Products'] = Product.objects.filter(category_id = ids)

		
		return render(request,'category.html',self.my_views)
