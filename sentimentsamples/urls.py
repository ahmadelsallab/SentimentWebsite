from django.conf.urls import url

from sentimentsamples import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
]