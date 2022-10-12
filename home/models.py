from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
# Our Products Category
class Category(models.Model):
	
	name = models.CharField(max_length = 200)
	# category id
	slug = models.CharField(max_length = 400,unique = True)
	logo = models.CharField(max_length = 200, blank = True)
	icon = models.CharField(max_length = 50,default = 'fa-home')
	def __str__(self):
		return f"< {self.name} >"


class SubCategory(models.Model):
	name = models.CharField(max_length = 400)
	slug = models.CharField(max_length = 300,unique = True)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)


	def __str__(self):
		return f"< {self.name} >"




STATUS = (
		('active','Active'),
		('default','Default'),
		)

class Slider(models.Model):
	slug = models.CharField(max_length = 90 , blank = True, unique = True)
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	description = models.TextField(blank = True)
	url = models.URLField(max_length = 500,blank = True)
	rank = models.IntegerField()
	status = models.CharField(choices = STATUS,max_length = 40)

	def __str__(self):
		return f"< {self.name} >"

class Ad(models.Model):
	slug = models.CharField(max_length = 90 , blank = True , unique = True)
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	url = models.URLField(max_length = 500,blank = True)
	rank = models.IntegerField(unique = True)
	
	def __str__(self):
		return f"< {self.name} >"




class Brand(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	slug = models.CharField(max_length = 400,blank = True ,unique = True)
	rank = models.IntegerField()
	
	def __str__(self):
		return f"< {self.name} >"

STOCK = (
		 ('in_stock','In Stock' ),
		 ('out_of_stock', 'Out Of Stock'),
		)

LABELS = (
		  ('new','New'),
	      ('hot','Hot'),
	      ('sale','Sale'),
 	      ('default','Default')
	     )

class Product(models.Model):
	pname = models.CharField(max_length = 500)
	price = models.IntegerField()
	slug = models.CharField(max_length = 500 , blank = True,unique = True)
	discount = models.IntegerField()
	image = models.ImageField(upload_to = 'media')
	description = models.TextField(blank = True)
	category = models.ForeignKey(Category , on_delete = models.CASCADE)
	sub_category = models.ForeignKey(SubCategory , on_delete = models.CASCADE)
	brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
	stock = models.CharField(choices = STOCK,max_length = 50)
	labels = models.CharField(choices = LABELS , max_length = 50)

	def __str__(self):
		return f"< {self.pname} >"

RATINGS = (
			(1,'1'),
			(2,'2'),
			(3,'3'),
			(4,'4'),
			(5,'5'),
		)		

class FeedBack(models.Model):
	author = models.CharField(max_length = 400)
	profession = models.CharField(max_length = 600)
	profile_pic = models.ImageField(upload_to = 'media')
	rating = models.IntegerField(choices = RATINGS)
	description = models.TextField() 

	def __str__(self):
		return f"< {self.author} >"



class Review(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	review = models.TextField(blank = True)
	rating = models.IntegerField(null = True)
	date = models.DateTimeField()
	slug = models.CharField(max_length = 500)

	def __str__(self):
		return f"< Review: {self.user.username}>"




