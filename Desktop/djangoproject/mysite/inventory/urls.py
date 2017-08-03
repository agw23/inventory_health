from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login, logout
from .views import HomeView
from .views import AutoDiscoverView
from .views import SingleDeviceView
from .views import Graph
from .views import BarGraph
from .views import ByOSCount
from .views import getDiagnosticsOptics
from .views import get_credentials
from .views import HorizontalChartSystemAlarms

from django.views.generic import TemplateView


urlpatterns = [
    #: /inventory/
    url(r'^$', get_credentials.as_view(), name='home'),

    url(r'^name/$', views.device, name='name'),

    url(r'^register/$', views.register , name='register'),

    url(r'^diagnostics-optics', getDiagnosticsOptics.as_view(), name='diagnostics-optics'),

    url(r'^add/$', HomeView.as_view(), name='add'),

    url(r'^saved/$', views.saved, name='saved'),

    url(r'^graph/$', Graph.as_view() , name='graph'),

    url(r'^visualdata/$', Graph.as_view(), name='graph'),

    url(r'^filter/$', views.filter, name='filter'),

    url(r'^countbyOS/$', ByOSCount.as_view(), name='filter'),

    url(r'^alarm_count/$', HorizontalChartSystemAlarms.as_view(), name='alarms'),

    url(r'^health/$', BarGraph.as_view(), name='health'),

    url(r'^discover/$', AutoDiscoverView.as_view(), name='discover'),

    url(r'^single/$', SingleDeviceView.as_view(), name='single'),

    url(r'^login/$', login, {'template_name': 'accounts/login.html'}),

    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}),
]
