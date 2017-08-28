# -*- coding: utf-8 -*-

from socket import gethostname
from django import forms
from django.core.validators import validate_email
from app.validators import validate_alnum,validate_int_digit,validate_port,validate_mem_gb
from app.cmd import LocalCommand

class EditorForm(forms.Form):

    form2edit = forms.CharField(label='', help_text='',
                                widget=forms.Textarea())

class Step01FormIndexNode(forms.Form):

    label = 'Would you like to continue?'

    title = '''Welcome to Cyber Defence Setup!<br />
This program will allow you to configure
Cyber Defence on {}.'''.format(gethostname())

    choices = [('0', 'Yes,Continue!'),
               ('1', 'No, Quit')]

    inq1 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())


class Step02FormIndexNode(forms.Form):

    label = 'Would you like to skip network configuration?'

    title = '''Its looks like /etc/network/interfaces has already been configured by this script.'''.format(gethostname())

    choices = [('0', 'Yes,skip network configuration!'),
               ('1', 'No, I need to reconfigure /etc/network/interfaces.')]

    inq2 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())

class Step03FormIndexNode(forms.Form):

    label = 'Component:'

    title = '''If this is the first machine in a distributed deployment,
choose Server.
<br />
This machine will only run Sguil, Squert, Snorby,
and Elasticsearch and will not monitor any network interfaces.
<br />
<br />
If this is a sensor for a distributed deployment (you've already installed
the Server), choose Sensor.
<br />
<br />
You will need to be able to SSH to the existing
Server box with an account with sudo privileges.
<br />
Otherwise, choose
Standalone to configure both Server and Sensor components on this box.'''

    choices = [('Indexnode', 'Indexnode')]

    inq3 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'INSTALLATION_TYPE'}))
    val = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IndexNode'}))
    
class Step04FormIndexNode(forms.Form):

    lc = LocalCommand()

    label = 'Memory in GB:'

    title = '''Please set up memory in GB for index node - on this server you
have free ~{}.<br />
Half of this value is deafult'''.format(lc.get_max_es_memory())

    inq4 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         initial='{}'.format(int(lc.get_max_es_memory()) / 2),
                         validators=[validate_mem_gb])   
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'ES_MEMORY'}))						 

						 
class Step05FormIndexNode(forms.Form):

    label = 'Would you like to continue?'

    title = '''Click Yes to make this change in file'''

    choices = [('0', 'Yes,Proceed with Change!'),
               ('1', 'No, Dont make any Change!')]

    inq5 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
