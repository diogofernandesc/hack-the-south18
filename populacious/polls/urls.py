from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
	# ex: /polls/
    url(r'^$', views.index, name='index'),
	# ex: /polls/5/
    url(r'^(?P<name>[a-zA-Z0-9]+)$', views.index, name='index')
]