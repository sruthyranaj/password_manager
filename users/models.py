from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Organizations(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return '<organization %s>' % self.name

class OrganizationsUsers(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'{self.organization.name} -  {self.user.username}'

