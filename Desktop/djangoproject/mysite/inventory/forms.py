from .models import IP
from .models import Autodiscover
from django import forms

from .models import Graph
from django.contrib.auth.models import User


#getting access to different inputs from the IP Model
class AddForm(forms.ModelForm):
    IP_address = forms.CharField(widget=forms.TextInput(
                                 attrs ={
                                     'class': 'form-control',


                               }
    ))

    class Meta:

        model = IP
        fields = ('IP_address',)

        exclude = ['IP_serial', 'version', 'model', 'uptime', 'IP_address_auto', 'password',]



class Register(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
                                 attrs ={
                                     'class': 'form-control',


                               }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',

        }
    ))

    class Meta:

        model = IP
        fields = ('username', 'password',)

        exclude = ['IP_serial', 'version', 'model', 'uptime', 'IP_address_auto', 'IP_address']





class GraphData(forms.ModelForm):
    IP_address = forms.CharField(widget=forms.TextInput(
                                 attrs ={
                                     'class': 'form-control',


                               }
    ))

    class Meta:

        model = Graph
        fields = ('IP_address',)




#getting access to different inputs from the Autodiscover Model
class AutoDiscover(forms.ModelForm):
    subnet = forms.CharField(widget=forms.TextInput(
                                 attrs ={
                                     'class': 'form-control',

                               }
    ))


    class Meta:
        model = Autodiscover
        fields = ('subnet',)


        exclude = ['port_status', 'ports', 'protocol', 'host',]





class SingleDeviceForm(forms.Form):

    yes_no = forms.BooleanField(required=False)

    #host = forms.CharField(widget=forms.HiddenInput(
     # attrs={
      # 'class':'form-control',
     #}
     #))
