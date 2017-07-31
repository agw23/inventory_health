from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login, logout
from .views import HomeView
from .views import LoginView
from .views import AutoDiscoverView
from .views import SingleDeviceView
from .views import Graph
from .views import BarGraph
from .views import ByOSCount
from .views import getDiagnosticsOptics
from .views import HorizontalChartSystemAlarms

from django.views.generic import TemplateView


urlpatterns = [
    #: /inventory/

    url(r'^$', views.index, name='home'),

    url(r'^name/$', views.device, name='name'),

    url(r'^register/$', views.register , name='register'),

    url(r'^diagnostics-optics', getDiagnosticsOptics.as_view(), name='diagnostics-optics'),

    url(r'^add/$', HomeView.as_view(), name='add'),

    url(r'^saved/$', views.saved, name='saved'),

    url(r'^graph/$', Graph.as_view() , name='graph'),

    url(r'^custom/$', LoginView.as_view(), name='customlogin'),

    url(r'^visualdata/$', Graph.as_view(), name='graph'),

    url(r'^filter/$', views.filter, name='filter'),

    url(r'^countbyOS/$', ByOSCount.as_view(), name='filter'),

    url(r'^alarm_count/$', HorizontalChartSystemAlarms.as_view(), name='alarms'),

    url(r'^health/$', BarGraph.as_view(), name='health'),

    url(r'^view/$', views.viewGraph, name='saved'),

    url(r'^discover/$', AutoDiscoverView.as_view(), name='discover'),

    url(r'^single/$', SingleDeviceView.as_view(), name='single'),

    url(r'^login/$', login, {'template_name': 'accounts/login.html'}),

    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}),
]
