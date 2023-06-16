from django.contrib import admin

from .models import Catalog, File, Section 

admin.site.register(Catalog)
admin.site.register(File)
admin.site.register(Section)
