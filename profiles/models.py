from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
# Create your models here.
from PIL import Image
from django.conf import settings
import os
from django.utils import timezone





class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        print("#########")

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        print("#########")
        return available
        

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles
    
# def upload_images_path(self, filename):
# 	return f'upload_images/{self.pk}/profile1.PNG'

def default_image():
	return "default_images/profile1.jpg"

def upload_images_path(instance, filename):
    profile_pic_name = 'user_{0}/profile1.PNG'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name


def default_image2():
	return "default_images/profile1.jpg"

def upload_images_path2(instance, filename):
    profile_pic_name2 = 'user_{0}/profile2.PNG'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name2)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name2



def default_image3():
	return "default_images/profile1.jpg"

def upload_images_path3(instance, filename):
    profile_pic_name3 = 'user_{0}/profile3.PNG'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name3)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name3
   

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
)

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=300)
    email = models.EmailField(max_length=200, blank=True, null= True, unique=True)
    address= models.CharField(max_length=200, blank=False)
    image = models.ImageField(default=default_image, upload_to=upload_images_path)
    image2 =  models.ImageField(default=default_image2, upload_to=upload_images_path2)
    image3 =  models.ImageField(default=default_image3, upload_to=upload_images_path3)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    nationalid= models.CharField(max_length=16, blank=True)
    telephone= models.CharField(max_length=10,  blank=False, unique=True,null= True)
    age= models.CharField(max_length=2, blank=True)
    gender = models.CharField(max_length=12, default="Your gender", choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True,blank=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    objects = ProfileManager()
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()
    
   
       
       

    # __initial_first_name = None
    # __initial_last_name = None

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__initial_first_name = self.first_name
    #     self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        # to_slug = self.slug
        # if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
        if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
        else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    
 
    
    

class Table(models.Model):
    TABLE_CATEGORIES = (
        ('YAC', 'TABLE 1'),
        ('NAC', 'TABLE 2'),
        ('DEL', 'TABLE 3'),
        ('KIN', 'TABLE 4'),
        ('QUE', 'TABLE 5'),
        ('TAC', 'TABLE 6'),
        ('MAC', 'TABLE 7'),
        ('XEL', 'TABLE 8'),
        ('GIN', 'TABLE 9'),
        ('WUE', 'TABLE 10'), 
        ('YAK', 'TABLE 11'),
        ('NOC', 'TABLE 12'),
        ('DEG', 'TABLE 13'),
        ('KIT', 'TABLE 14'),
        ('QUO', 'TABLE 15'), 
        ('GOC', 'TABLE 16'),
        ('JAC', 'TABLE 17'),
        ('DAL', 'TABLE 18'),
        ('KUN', 'TABLE 19'),
        ('QAE', 'TABLE 20'),
    )
    category = models.CharField(max_length=5, choices=TABLE_CATEGORIES)
    seats = models.IntegerField()
    

    def __str__(self):
        return f'seats={self.seats}. {dict(self.TABLE_CATEGORIES)[self.category]}'    
    
     
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()


    def __str__(self):
        return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'
    
    def get_table_category(self):
        table_categories=dict(self.table.TABLE_CATEGORIES)
        table_category= table_categories.get(self.table.category)  
        return table_category  
    
    def get_cancel_booking_url(self):  
        return reverse_lazy('profiles:CancelBookingView', args=[self.pk, ])
    
    
    
    
    
class Video(models.Model):
    caption = models.CharField(max_length=300)
    video = models.FileField(upload_to="video/%y")
    
    def __str__(self):
        return self.caption
    
    
class Contact(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    author = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.subject  


