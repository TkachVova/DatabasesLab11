from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from connect import Database
from App import tables
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
import forms

def index(request):
    database = Database()
    #database.drop_tables()
    #database.load_xml_data()
    table = tables.CarTable(database.get_all_from_car())
    RequestConfig(request).configure(table)
    return render(request, 'App/index.html', {'table': table})

def action(request):
    database = Database()
    if request.method == 'POST':
        action = request.POST.get('action', False)
        if action:
            pks = request.POST.getlist("selection")
            if action == 'delete':
                database.car_delete(pks)
                return HttpResponseRedirect('/')
            if action == 'load':
                return HttpResponseRedirect('/load_xml/')

        return HttpResponse('no POST in action view')

def add(request):
    database = Database()
    if request.method == 'POST':
        form = forms.CarAddForm(request.POST)
        if form.is_valid():
            database.car_insert(form.cleaned_data['producer'],
                                form.cleaned_data['model'],
                                form.cleaned_data['car_class'],
                                form.cleaned_data['drive'],
                                form.cleaned_data['engine'],
                                form.cleaned_data['interior'],
                                form.cleaned_data['body'],
                                form.cleaned_data['cost'],)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('form not valid')
    else:
        form = forms.CarAddForm()
    return render(request, 'App/add.html', {'form': form})

def car_detail(request, pk):
    database = Database()
    if request.method == 'POST':
        form = forms.CarAddForm(request.POST)
        if form.is_valid():
            database.car_edit(pk, form.cleaned_data['producer'],
                                form.cleaned_data['model'],
                                form.cleaned_data['car_class'],
                                form.cleaned_data['drive'],
                                form.cleaned_data['engine'],
                                form.cleaned_data['interior'],
                                form.cleaned_data['body'],
                                form.cleaned_data['cost'],)
            return HttpResponseRedirect('/')
    else:
        form = forms.CarAddForm(initial=database.get_car_instance(pk))
        return render(request, 'App/car_detail.html',  {'form': form, 'pk': pk})


def loadxml(request):
    database = Database()
    #database.drop_tables()
    database.load_xml_data()
    return HttpResponseRedirect('/')

def search(request):
    database = Database()
    if request.method == 'POST':
        cost = request.POST.get('cost', False)
        hpower = request.POST.get('hpower', False)
        interior = request.POST.get('interior', False)
        doors = request.POST.get('doors', False)
        table = tables.CarTable(database.formDataSearch(cost, hpower, interior, doors))
        RequestConfig(request).configure(table)
        return render(request, 'App/search.html', {'table': table})
    return HttpResponse("No POST")
