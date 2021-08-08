from django.contrib import admin
from .models import OrganizationsUsers, Organizations
# Register your models here.
admin.site.register(Organizations)
admin.site.register(OrganizationsUsers)