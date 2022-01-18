from django.urls import path
from .views import  enregistrer_paramSociete

urlpatterns = [
    path('search-record/', enregistrer_paramSociete, name="create-record"),
    

]
