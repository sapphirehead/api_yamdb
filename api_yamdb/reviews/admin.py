from django.contrib import admin
from .models import Categories, Genres, Title


admin.site.register(Title)
admin.site.register(Genres)
admin.site.register(Categories)
