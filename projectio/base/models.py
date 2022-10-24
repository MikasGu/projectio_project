from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Task(models.Model):
    name = models.CharField('Task name', max_length=100)
    info = models.CharField('Info', max_length=100)
    project = models.ForeignKey('Project', related_name='tasks', on_delete=models.SET_NULL, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    date = models.DateField('Date')
    sum = models.IntegerField('Sum')

    def __str__(self):
        return str(self.date)


class Employee(models.Model):
    f_name = models.CharField('First name', max_length=100)
    l_name = models.CharField('Last name', max_length=100)
    job = models.CharField('Job', max_length=100)

    phone = models.CharField('Phone', max_length=100, null=True)
    email = models.CharField('Email', max_length=100, null=True)
    pic = models.ImageField('Employee pic', upload_to='employee_pics', null=True, default='no-pic.png')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)

        if img.height > 50 or img.width > 50:
            output_size = (50, 50)
            img.thumbnail(output_size)
            quality_val = 90
            img.save(self.pic.path, quality=quality_val)

    def __str__(self):
        return self.f_name + ' ' + self.l_name


class Client(models.Model):
    f_name = models.CharField('First name', max_length=100)
    l_name = models.CharField('Last name', max_length=100)
    company = models.CharField('Company', max_length=100)
    contacts = models.CharField('Contacts', max_length=100)

    def __str__(self):
        return self.f_name + ' ' + self.l_name


class Project(models.Model):
    name = models.CharField('Name', max_length=100)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='projects')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    employees = models.ManyToManyField(Employee, related_name='projects')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    description = HTMLField()
    logo = models.ImageField('Project logo', upload_to='logos', null=True, default='no-image.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.logo.path)

        if img.height > 50 or img.width > 50:
            output_size = (50, 50)
            img.thumbnail(output_size)
            quality_val = 90
            img.save(self.logo.path, quality=quality_val)

    def __str__(self):
        return self.name
