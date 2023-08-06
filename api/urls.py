from django.urls import path
from api import views

urlpatterns = [
    path("alldata/", view=views.alldata, name="alldata"),
]
