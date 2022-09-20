from django.db import models

# Create your models here.
# Our Products Category
class Category(models.Model):
	
	name = models.CharField(max_length = 200)
	# category id
	slug = models.CharField(max_length = 400)
	logo = models.CharField(max_length = 200, blank = True)

	def __str__(self):
		return f"< {self.name} >"


class SubCategory(models.Model):
	name = models.CharField(max_length = 400)
	slug = models.CharField(max_length = 300)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)


	def __str__(self):
		return f"< {self.name} >"




STATUS = (
		('active','Active'),
		('default','Default'),
		)

class Slider(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	description = models.TextField(blank = True)
	url = models.URLField(max_length = 500,blank = True)
	rank = models.IntegerField()
	status = models.CharField(choices = STATUS,max_length = 40)

	def __str__(self):
		return f"< {self.name} >"

class Ad(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	url = models.URLField(max_length = 500,blank = True)
	
	def __str__(self):
		return f"< {self.name} >"




class Brand(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	slug = models.CharField(max_length = 400)
	rank = models.IntegerField()
	
	def __str__(self):
		return f"< {self.name} >"

STOCK = (
		('in_stock','In Stock' ),
		('out_of_stock', 'Out Of Stock'),
		)

LABELS = (
	( 'new','New'),
	('hot','Hot'),
	('sale','Sale'),
	('default','Default')
	)

class Product(models.Model):
	p_name = models.CharField(max_length = 500)
	price = models.IntegerField()
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


