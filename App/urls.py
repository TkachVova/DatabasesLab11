from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^action/$', views.action, name="action"),
    url(r'^add/$', views.add, name='add'),
    url(r'^car_detail/(\d+)/', views.car_detail, name='car_detail'),
    url(r'^load_xml/$', views.loadxml, name='load_xml'),
    url(r'^search/$', views.search, name='search'),
    url(r'^fulltext_search/$', views.fulltext_search, name='fulltext_search'),
)
