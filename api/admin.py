from django.contrib import admin

from .models import Comments, Posts

# Register your models here.
admin.site.register(Posts)
admin.site.register(Comments)
