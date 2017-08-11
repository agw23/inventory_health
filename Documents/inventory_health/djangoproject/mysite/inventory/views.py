# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

import sys
from jnpr.junos import Device
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.tools as tls
from plotly.graph_objs import *
import numpy as np
import plotly.figure_factory as FF
from lxml import etree

import nmap
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import plotly.figure_factory as ff
from plotly import tools

from .models import IP
from .models import Autodiscover
from .forms import SingleDeviceForm
from .models import Graph
from .forms import GraphData

from .forms import AddForm
from .forms import Login
from .forms import AutoDiscover
from django.views.generic import TemplateView

def index(request):

    template = loader.get_template('polls/index.html')
    C = create_user_data()
    dict = C.user_data()


    dict['username'] = request.POST.get('username')
    dict['password'] = request.POST.get('global_password')

    context = {
    }

    return HttpResponse(template.render(context, request))


class get_credentials(TemplateView):

    template_name = 'accounts/login.html'
    dict = []

    def get(self, request):
        login = Login()

        args = {'login': login}
        return render(request, self.template_name, args)

    def get_details(self, request):

        C = create_user_data()
        self.dict = C.user_data()
        self.dict['username'] = request.POST.get('username')
        self.dict['password'] = request.POST.get('global_password')

        username = self.dict['username']
        password = self.dict['password']

        request.session['username'] = username # set 'username' in the session
        request.session['password'] = password  # set 'password' in the session

        return self.dict

    def post(self, request):

        self.get_details(request)

        return render(request, 'polls/index.html')


class create_user_data():
        """
        :param username: username used to authenticate
        :param password: password used to authenticate
        """
        username = None
        password = None
        user_credentials = {}

        def user_data(self):
            self.user_credentials = {
            "username": self.username,
            "password": self.password,
        }
            return self.user_credentials



class HomeView(TemplateView):
    template_name = 'polls/home.html'

    def get(self, request):
        addform = AddForm()
        login = Login()

        posts = IP.objects.all()
        args = {'addForm': addform, 'login': login, 'details': posts}
        return render(request, self.template_name, args)


    def post(self, request):
        addform = AddForm(request.POST)
        login = Login(request.POST)

        username = request.session['username']  # get 'username' from the session
        password = request.session['password']  # get 'password' from the session

        if addform.is_valid():
            IPF = addform.save(commit=False)
            text = addform.cleaned_data['IP_address']
            posts = IP.objects.all()

            dev = Device(host=text, user=str(username), password=str(password))

        try:
                dev.open()

                serial = dev.facts['serialnumber']
                version = dev.facts['version']
                model  = dev.facts['model']
                uptime = dev.facts['RE0']['up_time']


                IPF.IP_serial = serial
                IPF.version = version

                IPF.model = model

                IPF.uptime = uptime
                addform.save()


        except Exception as err:
                print "Unable to connect to host:,"
                sys.exit(1)

        args = {'addresses': posts,'myForm': addform, 'text': text, 'serial': serial,
                'version': version, 'model': model,
                'uptime': uptime, 'login': login}

        return render(request, 'accounts/add_form.html', args)



def register(request):

    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            Login.username = username
            Login.password = password

            form.save()
        return redirect('/inventory/')

    else:
        form = UserCreationForm()
        return render(request, 'accounts/reg_form.html', {'form': form})



class SingleDeviceView(TemplateView):
    template_name = 'polls/single_auto_discover_results.html'

    def get(self, request):
        single = AddForm()

        addresses = IP.objects.all()

        args = {'singleForm': single, 'addresses': addresses}

        return render(request, self.template_name, args)

    def post(self, request):

        if request.method == "POST":

                ips_checked = request.POST.get("retrieve")

                username = request.session['username']  # get 'username' from the session
                password = request.session['password']  # get 'password' from the session

                dev = Device(host=ips_checked, user=str(username), password=str(password))

                try:
                    dev.open()

                    serial = dev.facts['serialnumber']
                    version = dev.facts['version']
                    model = dev.facts['model']
                    uptime = dev.facts['RE0']['up_time']

                    vlanInfo = dev.rpc.get_virtual_chassis_statistics_information()

                    for vlan in vlanInfo.iter('vccp-statistics'):
                            packets_received = vlan.find('totals-information/packets-received').text
                            packets_sent = vlan.find('totals-information/packets-sent').text

                            interfaceInfo = dev.rpc.get_route_engine_information()

                    for v in interfaceInfo.iter('route-engine'):
                                cpu_idle = v.find('cpu-idle').text
                                cpu_user = v.find('cpu-user').text
                                cpu_interrupt = v.find('cpu-interrupt').text
                                cpu_background = v.find('cpu-background')



                except Exception as err:
                    print "Unable to connect to host:,"
                    sys.exit(1)

                args = {'ip_checked': ips_checked, 'serial': serial, 'model': model, 'uptime': uptime,
                   'packets_received':packets_received, 'packets_sent': packets_sent, 'version': version,'cpu_idle': cpu_idle,
                        'cpu_user':cpu_user, 'cpu_interrupt':cpu_interrupt, 'cpu_background': cpu_background,

                       }

                return render(request, self.template_name, args)


class AutoDiscoverView(TemplateView):

    template_name = 'polls/discover.html'

    def get(self, request):
        discover = AutoDiscover()
        args = {'discoverForm': discover}
        return render(request, self.template_name, args)

    def post(self, request):
        form = AutoDiscover(request.POST)
        auto = SingleDeviceForm(request.POST)

        if form.is_valid():

            text = form.cleaned_data['subnet']
            Autodiscover.subnet = text

            nm = nmap.PortScanner()
            nm.scan(text)
            hosts = nm.all_hosts()

            for host in hosts:

                singlehost = host

                form.save()

                state = nm[host].state()

                protocols = nm[host].all_protocols()
                for proto in protocols:
                    protocol = proto

                    lport = nm[host][proto].keys()

                    lport.sort()

                    for port in lport:

                        port = port

                        port_state = nm[host][protocol][port]['state']

                args = {'devices': hosts, 'singlehost': host,'state': state, 'protocol': protocol, 'port_state':
                port_state, 'lport': lport, 'port': port, 'auto': auto}

            return render(request, 'polls/discover_results.html', args)


"""
Creates Pie Chart for CPU User, CPU Idle
and TCP statistics once 'Retrieve Graphical information' POST request
is received.
"""
class Graph(TemplateView):
    template_name = 'polls/viewData.html'
    cpu_idle = None
    cpu_user = None
    list_data = None
    system_data = None
    total = None
    free = None
    inUse = None
    tcp_packets = None
    tcp_received = None

    packets_sent = None
    packets_received = None
    list_data_packets = None
    list_system_statistics = None
    dev = None
    address = None

    def get(self, request):

        form = GraphData()

        args = {'visualData': form}

        return render(request, self.template_name, args)

    def post(self, request):
        viewData = GraphData(request.POST)

        if request.method == "POST":
            username = request.session['username']  # get 'username' from the session
            password = request.session['password']  #get 'password' from the session

            self.address = request.POST.get("graph")

            if viewData.is_valid():
                self.address = viewData.cleaned_data['IP_address']

            Graph.IP_address = self.address

            self.dev = Device(host=self.address, user=str(username), password=str(password))
            context = self.get_context_data()

            return render(request, 'polls/graph.html', context)

    def get_data_packets(self):

        try:
            self.dev.open()
            vlanInfo = self.dev.rpc.get_virtual_chassis_adjacency_information()


        except Exception as err:
            print "Unable to connect to host:,"
            sys.exit(1)

        return self.list_data_packets

    def get_system_data(self):

        try:
            self.dev.open()
            systemMemory = self.dev.rpc.get_system_memory_information()

            for s in systemMemory.iter('system-memory-summary-information'):
                self.total = s.find('system-memory-total').text
                self.free = s.find('system-memory-free').text

                total = int(self.total)
                free = int(self.free)

                self.inUse = total - free
                self.system_data = [self.inUse, self.free]

        except Exception as err:
            print "Unable to connect to host:,"
            sys.exit(1)

        return self.system_data

    def get_data(self):

        try:
            self.dev.open()
            interfaceInfo = self.dev.rpc.get_route_engine_information()

            for v in interfaceInfo.iter('route-engine'):
                self.cpu_idle = v.find('cpu-idle').text
                self.cpu_user = v.find('cpu-user').text

                self.list_data = [self.cpu_user, self.cpu_idle]

        except Exception as err:
            print "Unable to connect to host:,"
            sys.exit(1)

        return self.list_data

    def get_statistics(self):

        try:
            self.dev.open()

            statisticsInfo = self.dev.rpc.get_statistics_information()

            for v in statisticsInfo.iter('statistics'):
                self.tcp_packets = v.find('tcp/packets-sent').text
                self.tcp_received = v.find('tcp/packets-received').text

                self.list_system_statistics = [self.tcp_packets, self.tcp_received]

        except Exception as err:
            print "Unable to connect to host:,"
            sys.exit(1)

        return self.list_system_statistics


    def get_context_data(self, **kwargs):

        ctx = super(Graph, self).get_context_data(**kwargs)

        values = self.get_data()
        value1 = self.get_system_data()
        value3 = self.get_data_packets()
        value2 = self.get_statistics()

        fig = {
            "data": [
                {
                    "values": values,
                    "labels": [
                        "CPU IDLE",
                        "CPU USER",

                    ],
                    "domain":{'x': [0, .48],
                       'y': [0, .49]},
                    "name": "CPU UTILIZATION",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },

                {
                    "values": value2,
                    "labels": [
                        "Packets Sent TCP",
                        "Packets Received TCP",

                    ],
                    "domain": {'x': [.52, 1],
                       'y': [0, .49]},
                    "name": "TCP System Statistics",
                    "hoverinfo": "label+percent+value",
                    "hole": .4,
                    "type": "pie"
                },


                {
                    "values": value1,
                    "labels": [
                        "System Memory In Use",
                        "System Memory Free",

                    ],
                    "text": "TCP System Memory",
                    "textposition": "inside",
                    "domain": {'x': [0, .48],
                       'y': [.51, 1]},
                    "name": "Memory Usage",
                    "hoverinfo": "label+percent",
                    "hole": .4,
                    "type": "pie"
                },

                {
                    "values": value3,
                    "labels": [
                        "VCCP Adjacency Information",
                        "State",

                    ],
                    "text": "TCP System Memory",
                    "textposition": "inside",
                    "domain": {'x': [0, .48],
                               'y': [.51, 1]},
                    "name": "Memory Usage",
                    "hoverinfo": "label+percent",
                    "hole": .4,
                    "type": "pie"
                },


            ],

            "layout": {
                "title": "Graphical Report for" + " " + self.address,
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "",

                    },

                    {
                        "font": {
                            "size": 20
                        },
                        "text": "",
                        "showarrow": False,

                    },

                    {
                        "font": {
                            "size": 20
                        },

                        "text": "",
                        "showarrow": False,

                    },


                    {
                        "font": {
                            "size": 20
                        },

                        "text": "",
                        "showarrow": False,

                    }

                ]
            }
        }

        div = opy.plot(fig, auto_open=False, output_type='div')


        ctx['graph'] = div

        return ctx


"""Creates Bar Graph to display switch count by type (QX or EX"""

class BarGraph(TemplateView):

    countEx = IP.objects.filter(model__startswith='EX').count()

    countQFX = IP.objects.filter(model__startswith='QFX').count()

    e = None
    list_data_EX = []
    total = None
    system_data = None
    free = None
    inUse = None
    template_name = 'polls/health.html'


    """Displays the graph, renders it in polls/health template"""
    def get_context_data(self, **kwargs):
        context = super(BarGraph, self).get_context_data(**kwargs)

        trace1 = go.Bar(x=['EX', 'QFX'], y=[self.countEx, self.countQFX],
                marker=dict(
                color=['rgb(158,202,225)', 'rgb(158, 270, 225)']
                )
            )

        data = [go.Bar(
            trace1
        )]

        div = opy.plot(data, auto_open=False, output_type='div')

        context['graph'] = div

        return context



"""Class for Horizontal Charts. Displays IP addresses against alarm count."""

class HorizontalChartSystemAlarms(TemplateView):

    def __init__(self):

        self.alarm_description_list = []

        self.master_list = []

        self.alarm_description = None

        self.d = None

        self.dev = None


    system_alarm_count = []

    system_alarm_description = []

    list_alarm_count_ = []

    alarm_count = None

    master_list = []

    ip_list = []

    my_dict = {}

    value = None

    data = IP.objects.all()

    username = None

    password = None

    template_name = 'polls/alarm_count.html'


    def post(self, request):

        if request.method == "POST":
            self.username = request.session['username']  # get 'username' from the session
            self.password = request.session['password']  # get 'password' from the session

            context = self.get_context_data()

        return render(request, 'polls/alarm_count.html', context)

    """Getter for getting statistics regarding alarm information. Returns a list with the alarms
        for each IP."""
    def get_statistics(self):

        for self.d in self.data:

            self.system_alarm_count.append(self.d.IP_address)

            self.dev = Device(host=str(self.d.IP_address), user=str(self.username), password=str(self.password))

            try:
                self.dev.open()
                alarmInfo = self.dev.rpc.get_system_alarm_information()

                for v in alarmInfo.iter('alarm-summary'):
                    self.alarm_count = v.find('active-alarm-count').text

                self.list_alarm_count_.append(self.alarm_count)


            except Exception as err:
                print "Unable to connect to host:,"
                sys.exit(1)

        return self.list_alarm_count_

    def get_description(self):

        for self.d in self.data:

            self.dev = Device(host=str(self.d.IP_address), user='shanzeh',password='Juniper123!')
            temp = HorizontalChartSystemAlarms()

            try:
                self.dev.open()

                alarmInfo = self.dev.rpc.get_system_alarm_information()

                for v in alarmInfo.iter('alarm-detail'):

                    self.alarm_description = v.find('alarm-description').text

                    temp.alarm_description_list.append(self.alarm_description)

                self.alarm_description_list = temp.alarm_description_list

                self.ip_list.append(str(self.d.IP_address))

                self.master_list.append(temp.alarm_description_list)

                self.my_dict = dict(zip(self.ip_list, self.master_list))

            except Exception as err:
                print "Unable to connect to host:,"
                sys.exit(1)

        return self.my_dict.items()


    def add(self, description):
            self.alarm_description_list.append(description)


    def get_context_data(self, **kwargs):

        context = super(HorizontalChartSystemAlarms, self).get_context_data(**kwargs)

        self.get_statistics()

        self.get_description()

        trace1 = go.Bar(x=self.list_alarm_count_,
                        y=self.system_alarm_count,
                        marker=dict(
                            color=['rgb(242,230,255)', 'rgb(229, 204, 225)',
                                   'rgb(215,179,255)', 'rgb(12, 0, 26)',
                                   'rgb(12, 0, 26)', 'rgb(12, 0, 26)',
                                   ]
                        )


        )

        data = [go.Bar(
           trace1,
           orientation= 'h'
            )
        ]

        title = "Alarm Count by IP<br>\
           "

        layout = Layout(
            title=title,  # set plot title
            showlegend=False,  # remove legend
           yaxis=YAxis(
                zeroline=False,  # remove thick line at y=0
                gridcolor='white'  # set grid color to white
            ),

       )

        fig = go.Figure(data=data, layout=layout)

        div = opy.plot(fig, auto_open=False, output_type='div')

        context ['items'] = self.my_dict.iteritems()

        context['graph'] = div

        return context


class getDiagnosticsOptics(TemplateView):

    template_name = 'polls/diagnostics_optics.html'

    dev  = None

    address = None


    def post(self, request):

        if request.method == "POST":

            addform = AddForm(request.POST)

            username = request.session['username']  # get 'username' from the session
            password = request.session['password']  #get 'password' from the session
            print username
            print password

            if addform.is_valid():
                ip  = addform.cleaned_data['IP_address']

                addform.IP_address = ip

            self.dev = Device(host=str(ip), user=str(username), password=str(password))

            interface_list = []
            try:
                self.dev.open()
                optics_diagnostics = self.dev.rpc.get_interface_optics_diagnostics_information()

                for interface in optics_diagnostics.findall('physical-interface'):
                    root = interface.find('optics-diagnostics')
                    name = interface.find('name').text
                    interface_list.append(name)

            except:
                print "Unable to connect to host:,"
                sys.exit(1)

            args = {'root': root, 'name': name, 'interface_list': interface_list}

            return render(request, self.template_name, args)


    def get_data(self, request):

        try:

            self.dev.open()

            optics_diagnostics = self.dev.rpc.get_interface_optics_diagnostics_information()
            interface_list = []
            for interface in optics_diagnostics.findall('physical-interface'):
                root = interface.find('optics-diagnostics')
                name =  interface.find('name').text
                interface_list.append(name)

        except:
            print "Unable to connect to host:,"
            sys.exit(1)

        #args = {'root': root, 'name': name, 'interface_list': interface_list}


        #return render(request, self.template_name, args)


"""Filters by OS Version. It displays inventory according to type
of switch."""
class ByOSCount(TemplateView):

     #filtering through django queryset, with model field 'version'
    exVersion1 = IP.objects.filter(version__startswith='12.3').count()
    exVersion2 = IP.objects.filter(version__startswith='11.2').count()
    listEXIPs = []
    exNames = None
    e = None

    exVersion1List = IP.objects.filter(version__startswith='12.3')
    exVersion2List = IP.objects.filter(version__startswith='11.2')

    QFXVersion2 = IP.objects.filter(version__startswith='13.2').count()
    QFXVersion1 = IP.objects.filter(version__startswith='13.1').count()

    template_name = 'polls/by_OS_type.html'

    def get_context_data(self, **kwargs):
        context = super(ByOSCount, self).get_context_data(**kwargs)

        fig = {
            "data": [
                {
                    "values": [self.exVersion1, self.exVersion2],
                    "labels": [
                        "12.3",
                        "11.2",
                    ],
                    "domain": {"x": [0, .48]},
                    "textinfo": 'value',
                    "text": self.exVersion1,
                    "hoverinfo": "",
                    "hole": .4,
                    "type": "pie"
                },

                {
                    "values": [self.QFXVersion1, self.QFXVersion2],
                    "labels": [
                        "13.1",
                        "13.2",

                    ],
                    "textinfo": 'value',
                    "textposition": "inside",
                    "domain": {"x": [.52, 2 ]},
                    "hoverinfo": "",
                    "hole": .4,
                    "type": "pie"
                }
                ],
            "layout": {
                "title": "Count by OS",
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "EX",
                        "x": 0.20,
                        "y": 0.5
                    },

                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "QFX",
                        "x": 0.8,
                        "y": 0.5
                    }
                ]
            }
        }

        div = opy.plot(fig, auto_open=False, output_type='div')

        context['graph'] = div

        return context


def device(request):

    args = {'user': request.user}

    return render(request, 'accounts/name.html', args)

def viewGraph(request):

    g = Graph()

    context = g.get_context_data()

    return render(request, 'polls/graph.html', context)

def saved(request):

    data = IP.objects.all()
    args = {'data': data}

    return render(request, 'polls/onedevice_results.html', args)


def filter(request):

    form = AddForm()

    context = { 'form': form}

    return render(request, 'polls/filter_table_health_options.html', context)


def single(request):

    data = IP.objects.all()

    args = {'data': data}
    return render(request, 'polls/single_auto_discover_results.html', args)
