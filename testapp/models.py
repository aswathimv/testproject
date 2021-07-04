from django.db import models
# from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings


# Create your models here.
class loginn(models.Model):
	fname=models.CharField(max_length=60, default="",blank=True)
	lname=models.CharField(max_length=60, default="",blank=True)
	email= models.EmailField(max_length=60, default="",unique=True)
	pwd=models.CharField(max_length=60, default="",blank=True)

class Items(models.Model):
	ProductName=models.CharField(max_length=200, default="",blank=True)
	QtyUnit=models.CharField(max_length=60, default="",blank=True)

class Customer(models.Model):
    TrdName=models.CharField(max_length=60, default="",blank=True)
    Gstid=models.CharField(max_length=60, default="",blank=True)
    Addr1= models.CharField(max_length=60, default="",blank=True)
    Addr2=models.CharField(max_length=60, default="",blank=True)
    Place=models.CharField(max_length=60, default="",blank=True)
    Pincode=models.CharField(max_length=60, default="",blank=True)

class itmcustomer(models.Model):
	pid=models.ForeignKey(Items,on_delete=models.CASCADE,null=True,default='',blank=True)
	cid=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,default='',blank=True)
	taxableAmount=models.FloatField(default=0)
	Quantity=models.FloatField(default=0)
	ProducctDesc=models.CharField(max_length=60, default="",blank=True)

class Order(models.Model):
	cid=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,default='',blank=True) # to trader information
	iid=models.ForeignKey(itmcustomer,on_delete=models.CASCADE,null=True,default='',blank=True)
	taxableAmount=models.FloatField(default=0)
	Quantity=models.FloatField(default=0)
	OtherValue=models.FloatField(default="",blank=True)
	VehicleNo=models.CharField(max_length=60, default="",blank=True)
	VehicleType=models.CharField(max_length=60, default="",blank=True)
