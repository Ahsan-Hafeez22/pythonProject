import csv
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import pandas as pd


class customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    age = models.CharField(max_length=5)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class book(models.Model):
    title = models.CharField(max_length=20)
    auther = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class extended(models.Model):
    id = models.OneToOneField(customer, primary_key=True, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return str(self.id)


@receiver(pre_delete, sender=customer)
def pic_removing(sender, instance, **kwargs):
    try:
        os.remove(instance.extended.img.path)
    except:
        pass


@receiver(pre_delete, sender=User)
def delete_log(sender, instance, **kwargs):
    with open('hello.csv', 'a', newline='') as ufile:
        writer = csv.writer(ufile)
        writer.writerow([instance.username, instance.id, datetime.now()])



@receiver(pre_delete, sender=book)
def delete_logForBook(sender, instance, **kwargs):
    with open('helloBook.csv', 'a', newline='') as ufile:
        writer = csv.writer(ufile)
        writer.writerow([instance.title, instance.auther, instance.pk, datetime.now()])


# @receiver(pre_delete, sender=User)
# def log(sender, instance, **kwargs):
#     user_log = [{
#         'Name of User': instance.get_full_name(),
#         'User Id': instance.id,
#         'DateTime': datetime.now()
#     }]
#     df = pd.DataFrame(user_log)
#     df.to_csv('user_log.csv', header=False, sep="|", index=False, mode='a')
