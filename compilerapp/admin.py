from django.contrib import admin

from .models import User, Catalog, File, Section 

admin.site.register(User)
admin.site.register(Catalog)
admin.site.register(File)
admin.site.register(Section)
