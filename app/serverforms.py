# -*- coding: utf-8 -*-

from socket import gethostname
from django import forms
from django.core.validators import validate_email
from app.validators import validate_alnum,validate_int_digit,validate_port,validate_mem_gb
from app.cmd import LocalCommand

class EditorForm(forms.Form):

    form2edit = forms.CharField(label='', help_text='',
                                widget=forms.Textarea())

class Step01FormServer(forms.Form):

    label = 'Would you like to continue?'

    title = '''Welcome to Cyber Defence Setup!<br />
This program will allow you to configure
Cyber Defence on {}.'''.format(gethostname())

    choices = [('0', 'Yes,Continue!'),
               ('1', 'No, Quit')]

    sq1 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())


class Step02FormServer(forms.Form):

    label = 'Would you like to skip network configuration?'

    title = '''Its looks like /etc/network/interfaces has already been configured by this script.'''.format(gethostname())

    choices = [('0', 'Yes,skip network configuration!'),
               ('1', 'No, I need to reconfigure /etc/network/interfaces.')]

    sq2 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())

class Step03FormServer(forms.Form):

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

    choices = [('Server', 'Server')]

    sq3 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'INSTALLATION_TYPE'}))
    val = forms.CharField(widget=forms.HiddenInput(attrs={'value':'Server'}))
    
                           

class Step04FormServer(forms.Form):

    label = 'Username:'

    title = '''What would you like your Sguil username to be?<br />This will be
        used when logging into Sguil, Squert.<br />Please use alphanumeric
        characters only.'''

    sq4 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         validators=[validate_alnum])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SGUIL_CLIENT_USERNAME'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    
        

class Step05FormServer(forms.Form):

    label = 'Email:'

    title = '''What is your email address?<br />
This will be used when logging into Snorby. '''

    sq5 = forms.CharField(label=label, max_length=255,
                         min_length=6, required=True,
                         validators=[validate_email])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SNORBY_EMAIL'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    

class Step06FormServer(forms.Form):

    label1 = 'Password:'

    label2 = 'Confirm password:'

    title = '''What would you like to set your password to?<br />
Password must be at least 6 characters.
Please use alphanumeric characters only!<br />
This password will be used for Sguil, Squert, Snorby.<br />
Once you've logged into these interfaces using this initial password,
you can change it in Sguil and Snorby.'''

    sq6 = forms.CharField(label=label1, max_length=255,
                          min_length=6, required=True,
                          widget=forms.PasswordInput,
                          validators=[validate_alnum])

    sq6b = forms.CharField(label=label2, max_length=255,
                          min_length=6, required=True,
                          widget=forms.PasswordInput,
                          validators=[validate_alnum])


    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SGUIL_CLIENT_PASSWORD'})) 
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('sq6')
        password2 = cleaned_data.get('sq6b')
        if password1 != password2:
            raise forms.ValidationError('Passwords didn\'t match!')
        
         


class Step07FormServer(forms.Form):

    label = 'Days:'

    title = '''How many days of data do you want to keep in your Sguil
database?<br />
This includes things like IDS alerts.<br />
If you need to change this later, you can change DAYSTOKEEP in
/etc/nsm/securityonion.conf.<br />
Please enter an integer. The default is 30 days.'''

    sq7 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         initial='30',
                         validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'DAYSTOKEEP'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    

class Step08FormServer(forms.Form):

    label = 'Days:'

    title = '''How many days of data do you want to repair
in your Sguil database?<br />
A daily cronjob stops Sguil, repairs the MySQL tables for
the last X days, and then starts Sguil back up.<br />
If you choose a higher value, Sguil will be down for longer.<br />
If you need to change this later, you can change DAYSTOREPAIR
in /etc/nsm/securityonion.conf.<br />
Please enter an integer. The default is 7 days.'''

    sq8 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='7',
                          validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'DAYSTOREPAIR'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    

class Step09FormServer(forms.Form):

    label = 'IDS Engine:'

    title = '''Suricata IDS Engine is only choise for now'''

    sq9 = forms.BooleanField(label=label, required=True)
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_ENGINE'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    

class Step10FormServer(forms.Form):

    label = 'IDF ruleset:'

    title = '''Which IDS ruleset would you like to use?'''

    choices = [('ETGPL', 'ETGPL'),
               ('ETPRO', 'ETPRO'),
               ('VRT', 'VRT'),
               ('VRTET', 'VRTET')]

    sq10 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_RULESET'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    


class Step11FormServer(forms.Form):

    label = 'Port:'

    title = '''Please specificity on which port sensor should sent logs stream
to Server - should be the same as it was set on server.<br /><br />
The default is 5043 tcp port.
Please use range: 1-65535 only.  '''

    sq11 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='5043',
                          validators=[validate_port])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'LOGSTASH_REDIS_PORT'}))
    
    
class Step12FormServer(forms.Form):

    lc = LocalCommand()

    label = 'Memory in GB:'

    title = '''Please set up memory in GB for Elastic node - on this server you
have free ~{}.<br />
Half of this value is deafult'''.format(lc.get_max_es_memory())

    sq12 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         #initial='{}'.format(int(100) / 2),
                         validators=[validate_mem_gb])
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'ES_MEMORY'}))


class Step13FormServer(forms.Form):

    label = 'Enable Salt:'

    title = '''Salt can be enabled to help manage your entire sensor
deployment.<br /><br />By default, Salt will automatically keep
the following updated:<br />
* OS user accounts
* SSH keys for those user accounts<br />
* IDS rulesets<br />
<br />
Salt can also be used for remote execution, so you can run a command<br />
and have it execute on all sensors across your deployment.<br />
Would you like to enable Salt?'''

    choices = [('0', 'Yes,Enable Salt!'),
               ('1', 'No, Diable Salt')]

    sq13 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())

    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SALT'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))



class Step14FormServer(forms.Form):

    label = 'Would you like to continue?'

    title = '''Click Yes to make this change in file'''

    choices = [('0', 'Yes,Proceed with Change!'),
               ('1', 'No, Dont make any Change!')]

    sq14 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    



