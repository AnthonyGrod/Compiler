from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.sessions.backends.db import SessionStore

from .models import Catalog, File, Section

from datetime import datetime

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
    session = SessionStore(request.session.session_key)
    # catalogs = Catalog.objects.all()
    root = Catalog.objects.filter(parent=None, is_deleted=False, user=request.user)
    if (len(root) != 1):
        root = Catalog.objects.create(name='root', parent=None, user=request.user)
        root.save()
    else:
        root = root[0]
    file_tree = root.return_nested_objects()
    context = {
        'file_tree': file_tree,
        'root': root,
    }
    print(request.method)
    if request.method == 'POST':
        if "file" in request.POST:
            file_id = request.POST['file']
            file = File.objects.get(id=file_id)
            file_content = file.content
            session['file_content'] = file_content
        if "standard" in request.POST:
            session['standard'] = request.POST['standard']
            # context.update({'standard': request.POST['standard']})
        if "optymalization" in request.POST:
            session['selected_optymalizations'] = request.POST.getlist('optymalization')
        if "procesor" in request.POST:
            session['procesor'] = request.POST['procesor']
        if "procesor_options" in request.POST:
            print("=====================================")
            print(request.POST.getlist('procesor_options'))
            session['procesor_options'] = request.POST.getlist('procesor_options')

    # Retrieve the stored data from the session
    if "standard" in session:
        context.update({'standard': session['standard']})

    if "selected_optymalizations" in session:
        context.update({'selected_optymalizations': session['selected_optymalizations']})

    if "file_content" in session:
        context.update({'file_content': session['file_content']})

    if "procesor" in session:
        context.update({'procesor': session['procesor']})

    if "procesor_options" in session:
        context.update({'procesor_options': session['procesor_options']})
    
    session.save()
    print(context)

            
    return render(request, 'index.html', context)

def add_catalog(request):
    if request.method == 'GET':
        context = {
            'catalogs': Catalog.objects.filter(user=request.user),
        }
        return render(request, 'add_catalog.html', context)
    elif request.method == 'POST':
        name = request.POST['catalog_name']
        description = request.POST['catalog_description']
        parent = request.POST['parent_catalog']
        if name == '' or parent == '':
            return HttpResponseRedirect(reverse('compilerapp:index'))
        else:
            parent = Catalog.objects.get(id=parent)
        catalog = Catalog.objects.create(name=name, description=description, parent=parent, user=request.user)
        catalog.save()
        return HttpResponseRedirect(reverse('compilerapp:index'))
    
def add_file(request):
    if request.method == 'GET':
        context = {
            'catalogs': Catalog.objects.filter(user=request.user),
        }
        return render(request, 'add_file.html', context)
    elif request.method == 'POST':
        name = request.POST['file_name']
        description = request.POST['file_description']
        catalog = request.POST['parent_catalog']
        content = request.POST['file_content']
        if catalog == '' or name == '':
            return HttpResponseRedirect(reverse('compilerapp:index'))
        else:
            catalog = Catalog.objects.get(id=catalog)
        file_to_create = File.objects.create(name=name, description=description, catalog=catalog, user=request.user, content=content)
        file_to_create.save()
        return HttpResponseRedirect(reverse('compilerapp:index'))
    
def delete_file(request):
    if request.method == 'GET':
        context = {
            'files': File.objects.filter(user=request.user),
        }
        return render(request, 'delete_file.html', context)
    elif request.method == 'POST':
        file_id = request.POST['file_to_delete']
        file_to_delete = File.objects.get(id=file_id)
        file_to_delete.deleted_at = datetime.now()
        file_to_delete.is_deleted = True
        file_to_delete.save()
        return HttpResponseRedirect(reverse('compilerapp:index'))
    
def delete_catalog(request):
    if request.method == 'GET':
        context = {
            'catalogs': Catalog.objects.filter(user=request.user),
        }
        return render(request, 'delete_catalog.html', context)
    elif request.method == 'POST':
        catalog_id = request.POST['catalog_to_delete']
        catalog_to_delete = Catalog.objects.get(id=catalog_id)
        catalog_to_delete.deleted_at = datetime.now()
        catalog_to_delete.is_deleted = True
        catalog_to_delete.save()
        return HttpResponseRedirect(reverse('compilerapp:index'))