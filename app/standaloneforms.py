# -*- coding: utf-8 -*-

from socket import gethostname
from django import forms
from django.core.validators import validate_email
from app.validators import validate_alnum,validate_int_digit,validate_port,validate_mem_gb,validate_range_10_100
from app.cmd import LocalCommand

class EditorForm(forms.Form):

    form2edit = forms.CharField(label='', help_text='',
                                widget=forms.Textarea())

class Step01FormStandalone(forms.Form):

    label = 'Would you like to continue?'

    title = '''Welcome to Cyber Defence Setup!<br />
This program will allow you to configure
Cyber Defence on {}.'''.format(gethostname())

    choices = [('0', 'Yes,Continue!'),
               ('1', 'No, Quit')]

    saq1 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())


class Step02FormStandalone(forms.Form):

    label = 'Would you like to skip network configuration?'

    title = '''Its looks like /etc/network/interfaces has already been configured by this script.'''.format(gethostname())

    choices = [('0', 'Yes,skip network configuration!'),
               ('1', 'No, I need to reconfigure /etc/network/interfaces.')]

    saq2 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())

class Step03FormStandalone(forms.Form):

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

    choices = [('Standalone', 'Standalone')]

    saq3= forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'INSTALLATION_TYPE'}))
    val = forms.CharField(widget=forms.HiddenInput(attrs={'value':'Standalone'}))
    
                           
    
class Step04FormStandalone(forms.Form):

    label = 'Username:'

    title = '''What would you like your Sguil username to be?<br />This will be
        used when logging into Sguil, Squert.<br />Please use alphanumeric
        characters only.'''

    saq4 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         validators=[validate_alnum])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SGUIL_CLIENT_USERNAME'}))
    
class Step05FormStandalone(forms.Form):

    label = 'Email:'

    title = '''What is your email address?<br />
This will be used when logging into Snorby. '''

    saq5 = forms.CharField(label=label, max_length=255,
                         min_length=6, required=True,
                         validators=[validate_email])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SNORBY_EMAIL'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))


class Step06FormStandalone(forms.Form):

    label1 = 'Password:'

    label2 = 'Confirm password:'

    title = '''What would you like to set your password to?<br />
Password must be at least 6 characters.
Please use alphanumeric characters only!<br />
This password will be used for Sguil, Squert, Snorby.<br />
Once you've logged into these interfaces using this initial password,
you can change it in Sguil and Snorby.'''

    saq6 = forms.CharField(label=label1, max_length=255,
                          min_length=6, required=True,
                          widget=forms.PasswordInput,
                          validators=[validate_alnum])

    saq6b = forms.CharField(label=label2, max_length=255,
                          min_length=6, required=True,
                          widget=forms.PasswordInput,
                          validators=[validate_alnum])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SGUIL_CLIENT_PASSWORD'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('saq6')
        password2 = cleaned_data.get('saq6b')
        if password1 != password2:
            raise forms.ValidationError('Passwords didn\'t match!')


class Step07FormStandalone(forms.Form):

    label = 'Days:'

    title = '''How many days of data do you want to keep in your Sguil
database?<br />
This includes things like IDS alerts.<br />
If you need to change this later, you can change DAYSTOKEEP in
/etc/nsm/securityonion.conf.<br />
Please enter an integer. The default is 30 days.'''

    saq7 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         initial='30',
                         validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'DAYSTOKEEP'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    
class Step08FormStandalone(forms.Form):

    label = 'Days:'

    title = '''How many days of data do you want to repair
in your Sguil database?<br />
A daily cronjob stops Sguil, repairs the MySQL tables for
the last X days, and then starts Sguil back up.<br />
If you choose a higher value, Sguil will be down for longer.<br />
If you need to change this later, you can change DAYSTOREPAIR
in /etc/nsm/securityonion.conf.<br />
Please enter an integer. The default is 7 days.'''

    saq8 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='7',
                          validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'DAYSTOREPAIR'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))        


class Step09FormStandalone(forms.Form):

    label = 'IDS Engine:'

    title = '''Suricata IDS Engine is only choise for now'''

    saq9 = forms.BooleanField(label=label, required=True)
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_ENGINE'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    


class Step10FormStandalone(forms.Form):

    label = 'IDF ruleset:'

    title = '''Which IDS ruleset would you like to use?'''

    choices = [('ETGPL', 'ETGPL'),
               ('ETPRO', 'ETPRO'),
               ('VRT', 'VRT'),
               ('VRTET', 'VRTET')]

    saq10 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_RULESET'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))

class Step11FormStandalone(forms.Form):

    label = 'Snort VRT oinkcode:'

    title = '''Please enter your Snort VRT oinkcode.<br /><br />
If you don't already have one, you can obtain one from
http://www.snort.org/.'''

    saq11 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True)
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'OINKCODE'}))


class Step12FormStandalone(forms.Form):

    label = 'Port:'

    title = '''Please specificity on which port sensor should sent logs stream
to Server - should be the same as it was set on server.<br /><br />
The default is 5043 tcp port.
Please use range: 1-65535 only.  '''

    saq12 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='5043',
                          validators=[validate_port])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'LOGSTASH_REDIS_PORT'}))

                

class Step13FormStandalone(forms.Form):

    lc = LocalCommand()

    label = 'Memory in GB:'

    title = '''Please set up memory in GB for Elastic node - on this server you
have free ~{}.<br />
Half of this value is deafult'''.format(lc.get_max_es_memory())

    saq13 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         initial='{}'.format(int(100) / 2),
                         validators=[validate_mem_gb])
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'ES_MEMORY'}))


class Step14FormStandalone(forms.Form):

    label = 'Port:'

    title = '''What would you like to set PF__RING min__num__slots to?<br /><br />
The default is 4096.  For busy networks, you may want to increasethis to
a higher number like 65534.<br /><br />If you need to change this later,
you can modify /etc/modprobe.d/pf__ring.conf and reload the pf_ring module.'''

    saq14 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='4096',
                          validators=[validate_port])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PF_RING_SLOTS'}))
    

class Step15FormStandalone(forms.Form):

    choices = [('eth0', 'eth0'),
                ('eth1', 'eth1')]

    label = 'Network interface(s):'

    title = '''Which network interface(s) should be monitored?<br /><br />
If you allowed Setup to configure /etc/network/interfaces,
your monitor interfaces are already selected.'''

    saq15 = forms.MultipleChoiceField(label=label, required=True,
                                    choices=choices,
                                    widget=forms.CheckboxSelectMultiple())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'INTERFACES'}))
                                    
    

class Step16FormStandalone(forms.Form):

    label = 'Enable IDS Engine:'

    title = '''The IDS Engine (Snort/Suricata) listens on the interfaces<br />
specified on the previous screen and logs IDS alerts.<br /><br />
Would you like to enable the IDS Engine?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    saq16 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_ENGINE_ENABLED'}))

class Step17FormStandalone(forms.Form):

    label = 'Number of IDS engine processes:'

    title = '''How many IDS engine processes would you like to run?<br /><br />
This is limited by the number of CPU cores on your system.<br /><br />
If you need to change this setting later, change IDS_LB_PROCS
in /etc/nsm/HOSTNAME-INTERFACE/sensor.conf'''
    
    choices = [(1, 1),
               (2, 2),
               (3, 3)]
    
    
    saq17 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_LB_PROCS'}))


class Step18FormStandalone(forms.Form):

    label = 'Enable Bro:'

    title = '''Bro listens on the chosen interfaces and writes protocol logs.<br /><br />
Would you like to enable Bro?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    saq18 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'BRO_ENABLED'}))


class Step19FormStandalone(forms.Form):

    label = 'Enable file extraction:'

    title = '''Bro can extract files (EXEs by default) from your network
traffic.<br /><br />If enabled, EXEs will be stored in
/nsm/bro/extracted/.<br />
Would you like to enable file extraction?<br />'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    saq19 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'EXTRACT_FILES'}))


class Step20FormStandalone(forms.Form):
   
    label = 'Number of Bro processes:'

    title = '''How many Bro processes would you like to run?<br /><br />
This is limited by the total number of CPU cores on your system,<br />
but you should probably choose no more than HALF
your number of CPU cores.<br /><br />
If you need to change this setting later, you can change the lb_procs variable
in /opt/bro/etc/node.cfg.'''

    choices = [(1, 1),
               (2, 2),
               (3, 3)]
    saq20 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'BRO_LB_PROCS'}))


class Step21FormStandalone(forms.Form):

    label = 'Enable full packet capture:'

    title = '''Full packet capture writes all monitored traffic to disk.<br /><br />
Full packet capture requires lots of disk space,<br />
but gives you lots of forensic capabilities<br />
and is therefore highly recommended!<br />
Would you like to enable full packet capture?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    saq21 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_ENABLED'}))

class Step22FormStandalone(forms.Form):

    label = 'File size:'

    title = '''How big do you want your pcap files to be?<br /><br />
Please enter an integer in Megabytes (MB). The default is 150 MB.'''

    saq22 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='150',
                          validators=[validate_int_digit])
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_SIZE_CONFIRMED'}))

class Step23FormStandalone(forms.Form):

    label = 'Enable mmap I/O:'

    title = '''netsniff-ng defaults to using scatter/gather pcap file I/O.<br /><br />
For higher performance, you can enable mmap I/O,
but this requires more RAM.<br />Would you like to enable mmap I/O?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    saq23 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_OPTIONS'}))
                            
class Step24FormStandalone(forms.Form):

    label = 'PCAP ring buffer size:'

    title = '''How large do you want your PCAP ring buffer?<br /><br />
Each monitoring interface will have the specified amount allocated from
RAM<br />so be sure your system has enough memory. In the case of 4 sensor
interfaces<br />and a specified ring buffer of 1GB, 4GB of total RAM will
be allocated for packet<br />buffering. For busy networks a ring buffer
of at least 256MB is recommended.<br /><br />
Please enter an integer in Megabytes (MB). The default is 64 MB.<br />
How large do you want your PCAP ring buffer?'''

    saq24 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='64',
                          validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_RING_SIZE'}))


class Step25FormStandalone(forms.Form):

    label = '''Percent:'''

    title = '''At what percent of disk usage would you like to begin
purging old logs?<br /><br />
Please enter an integer between 10 and 100.  The default is 90.'''

    saq25 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='90',
                          validators=[validate_range_10_100])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'CRIT_DISK_USAGE'}))



class Step26FormStandalone(forms.Form):

    label = 'Would you like to continue?'

    title = '''Click Yes to make this change in file'''

    choices = [('0', 'Yes,Proceed with Change!'),
               ('1', 'No, Dont make any Change!')]

    saq26 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    



