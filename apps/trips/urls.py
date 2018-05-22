from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin', views.signin),
    url(r'^register$', views.register),
    url(r'^register/process$', views.register_process),
    url(r'^profile$', views.profile),
    url(r'^trips/new$', views.newTrip),
    url(r'^trips/new/process$', views.newTrip_process),
    url(r'^trips/plan/(?P<tripID>\d+)$', views.plan),
    url(r'^logout$', views.logout),
    url(r'^try$', views.tryIt),

]
