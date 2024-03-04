from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _



class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Myusers(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    #Phone_no=models.IntegerField(blank=True,null=True)
    #image = models.ImageField(upload_to=None,default='static/image.jpg', blank=True, null=True)
    #vehicle=models.CharField(max_length=10,unique=True,blank=True,null=True)
    #city=models.CharField(max_length=255,blank=True,null=True)
    #state=models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return self.first_name+' '+self.last_name

class UserProfile(models.Model):
    user = models.OneToOneField(Myusers, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default='')
    phoneNumber = models.IntegerField(default=0)
    reward_coins = models.IntegerField(default=0)
    pincode = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', default='images.jpeg', blank=True)

    def _str_(self):
        return str(self.user.__str__()) + "Profile"


def createProfile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(createProfile, sender=Myusers)
class Vehicle(models.Model):
    user=models.ForeignKey(Myusers,on_delete=models.CASCADE)
    vehicle_name=models.CharField(max_length=50)
    vehicle_no = models.CharField(max_length=8,unique=True)

    def __str__(self):
        return self.user.__str__()+self.vehicle_name


class RentRegister(models.Model):
    user = models.ForeignKey(Myusers, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=100, default=' ')
    address = models.CharField(max_length=100)
    total_transport = models.PositiveIntegerField(default=0, blank=True, null=True)
    money_per_hour = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_money=models.CharField(max_length=300,default=0)
    occupied_transport = models.PositiveIntegerField(default=0, blank=True, null=True)
    latitude = models.CharField(default=1,max_length=50, blank=True, null=True)
    longitude = models.CharField(default=1,max_length=50, blank=True, null=True)
    hold= models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name+' '+self.address

    @property
    def balance_car(self):
        return self.total_transport-self.occupied_transport

class RentImages(models.Model):
    rentuser = models.ForeignKey(RentRegister, on_delete=models.CASCADE, default=None)
    images = models.FileField(upload_to='RentImages', blank=True, verbose_name='Image')

    def __str__(self):
        return str(self.rentuser)+"_"+str(self.images)

class SlotsPlace(models.Model):
    user = models.ForeignKey(Myusers, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=100, default=' ')
    slot_name = models.CharField(max_length=100, default=' ')
    slot_available = models.BooleanField(default=True)
    value = models.CharField(max_length=100, default='1')
    edited = models.CharField(max_length=100, default='1')
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-createdAt']

    def __str__(self):
        return self.slot_name + '-' + self.value + '-' + self.place_name + '-' + self.edited


class Booking(models.Model):
    customer=models.ForeignKey(Myusers,on_delete=models.CASCADE)
    slot_name = models.CharField(max_length=100, default=' ')
    vehicle = models.CharField(max_length=10,blank=True,null=True,unique=True)
    amount_to_pay = models.PositiveIntegerField(blank=True, null=True)
    booked = models.BooleanField(default=False)
    booked_place = models.ForeignKey(RentRegister,models.CASCADE,blank=True,null=True)
    no_of_hours = models.PositiveIntegerField(default=0, blank=True, null=True)
    booked_at = models.DateTimeField(default=None, blank=True, null=True)
    ending_at = models.DateTimeField(default=None, blank=True, null=True)
    class Meta:
        ordering=['-booked_at']

    def __str__(self):
        return self.customer.__str__() + str(self.no_of_hours)
        # return str(self.no_of_hours)



class Report(models.Model):
    user = models.ForeignKey(Myusers, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    transport_number = models.CharField(max_length=10,default=0)
    description = models.TextField(max_length=450)
    created_at = models.DateTimeField(auto_now_add=True)
    verified=models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return self.user.__str__()


class ReportImages(models.Model):
    reportuser = models.ForeignKey(Report, on_delete=models.CASCADE, default=None)
    images = models.FileField(upload_to='ReportImages', blank=True, verbose_name='report_images')

    def _str_(self):
        return str(self.reportuser)+"_"+str(self.images)



''' vehicle=models.CharField(max_length=10,unique=True)
    #vehicle_model = models.CharField(max_length=50)
    amount_to_pay=models.PositiveIntegerField(blank=True,null=True)
    booked=models.BooleanField(default=False)
    booked_place=models.ForeignKey(Rent,on_delete=models.CASCADE,null=True,blank=True)
    no_of_hours=models.PositiveIntegerField(default=0,blank=True,null=True)
    booked_at=models.DateTimeField(default=None,blank=True,null=True)
    ending_at=models.DateTimeField(default=None,blank=True,null=True)

    def __str__(self):
        return self.customer.__str__()+str(self.no_of_hours)
        #return str(self.no_of_hours)
    @property
    def expired(self,current_time):
        if self.ending_at<current_time:
            return True
        return False
'''