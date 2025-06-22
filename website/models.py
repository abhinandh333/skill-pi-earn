from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.db import models
from django.contrib.auth import get_user_model
from datetime import date


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, phone_number=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email, full_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 👇 Add user type field
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('owner', 'Shop/Enterprise Owner'),
        ('normal', 'Normal User'),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="User Type"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('shop_owner', 'Shop/Enterprise Owner'),
            ]
      
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    alt_number = models.CharField(max_length=15, blank=True, null=True)  # if still used
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
    upload_to='profile_pics/',
    default='profile_pics/default.jpg',
    blank=True,
    null=True)


    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)


    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __str__(self):
        return self.user.email



    def average_rating(self):
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 1) if avg else 0

    def rating_count(self):
        return self.reviews.count()




class ProductImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models
from django.utils import timezone
from .models import Profile  # assuming Profile exists

class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.profile.user.email} by {self.reviewer_name}"

