from django.urls import path
from .views import *

urlpatterns = [
	path('',home,name="home"),
	path('getText',getText,name='getText'),
	path('rdf',rdf,name='rdf')
]