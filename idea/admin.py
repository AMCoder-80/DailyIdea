from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Idea)
admin.site.register(models.Category)
admin.site.register(models.Requester)
