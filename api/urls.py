from django.urls import path
from api.views.crime import (
    alldata,
    battery,
    getmap,
    getareas,
    getclusters,
    getbarpolar,
    get_crime,
    getdotdata
)

urlpatterns = [
    path("alldata/", view=alldata, name="alldata"),
    path("battery/", view=battery, name="battery"),
    path("getmap/", view=getmap, name="getmap"),
    path("getareas/", view=getareas, name="getareas"),
    path("getclusters/", view=getclusters, name="getclusters"),
    path("getbarpolar/", view=getbarpolar, name="getbarpolar"),
    path("getcrime/", view=get_crime, name="getcrime"),
    path("getdotdata/", view=getdotdata, name="getdotdata"),
]
