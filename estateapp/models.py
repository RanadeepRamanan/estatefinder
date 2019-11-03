# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


 
 
class MyAccountManager(BaseUserManager):
 
    def create_user(self,email,username,phone,name,password=None):

        if not email:
            raise ValueError()
        if not username:
            raise ValueError()
        user  = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
            phone = phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password, phone=None,name=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
  
class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email",max_length=255,unique=True)
    #required as it is for custom user imp****
    username        = models.CharField(max_length=30,unique=True)
    date_joined     = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    #*******required as it is for custom user imp
    phone           = models.CharField(max_length=10, default='', editable=False,)
    name            = models.CharField(max_length=50, default='', editable=False,)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone', 'name']
    objects = MyAccountManager()
 
    def __str__(self):
        return self.email
   
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


class pgmodel(models.Model):
   
    user_id=models.ForeignKey(Account, on_delete=models.CASCADE,  default='', editable=False)
    mobile=models.CharField(max_length=10)
    city=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    CHOICES1=(
        ('female','Female'),
        ('male','Male'),
        ('any','Any')
    )
    CHOICES2=(
        ('single','Single'),
        ('sharing','Sharing')
        
    )
    balcony= (
    ('yes', 'Yes'),
    ('no', 'No')
    
    )
    parking= (
    ('yes', 'Yes'),
    ('no', 'No')
    
    )
    box=(
        
        ('A.C', 'A.C'),
        ('TV', 'TV'),
        ('Fridge', 'Fridge'),
        ('Washing Machine','Washing Machine'),
        ('Wi-fi','Wi-fi')
    )
    food=(
       ('yes', 'Yes') ,
       ('no', 'No')
    )
   
    
    
    available=models.CharField(choices=CHOICES1, max_length=100 ,default='', editable=False)
    occupancy=models.CharField(choices=CHOICES2, max_length=100)
    balcony=models.CharField(choices=balcony, max_length=100)
    parking=models.CharField(choices=parking, max_length=100)
    food=models.CharField(choices=food,default='', editable=False, max_length=100)
    amount=models.CharField( max_length=100)
    details=MultiSelectField(choices=box, default='', editable=False, max_length=100)

    # def __str__(self):
    #     return str(self.id)
    
    
