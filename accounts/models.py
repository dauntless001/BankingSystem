from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
# Create your models here.

gender = (
    ('Male','Male'),
    ('Female', 'Female'), 
)


def get_secret_num():
    value = random.randint(1111111111, 9999999999)
    return value

class User(AbstractUser):
    pass

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    sec_num = models.IntegerField(default=get_secret_num())
    acc_bal = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, choices=gender)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()



class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return self.user.username