from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Catalog, File, Section

def index(request):
    catalogs_list = Catalog.objects.order_by('-created_at')[:]
    template = loader.get_template('compilerapp/index.html')
    context = {
        'catalogs_list': catalogs_list,
    }
    return HttpResponse(template.render(context, request))
