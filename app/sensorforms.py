# -*- coding: utf-8 -*-

from socket import gethostname
from django import forms
from django.core.validators import validate_email
from app.validators import validate_alnum,validate_int_digit,validate_port,validate_mem_gb,validate_range_10_100


class EditorForm(forms.Form):

    form2edit = forms.CharField(label='', help_text='',
                                widget=forms.Textarea())

class Step01FormSensor(forms.Form):

    label = 'Would you like to continue?'

    title = '''Welcome to Cyber Defence Setup!<br />
This program will allow you to configure
Cyber Defence on {}.'''.format(gethostname())

    choices = [('0', 'Yes,Continue!'),
               ('1', 'No, Quit')]

    snq1 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())


class Step02FormSensor(forms.Form):

    label = 'Would you like to skip network configuration?'

    title = '''Its looks like /etc/network/interfaces has already been configured by this script.'''.format(gethostname())

    choices = [('0', 'Yes,skip network configuration!'),
               ('1', 'No, I need to reconfigure /etc/network/interfaces.')]

    snq2 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())

class Step03FormSensor(forms.Form):

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

    choices = [('Sensor', 'Sensor')]

    snq3 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'INSTALLATION_TYPE'}))
    val = forms.CharField(widget=forms.HiddenInput(attrs={'value':'Sensor'}))
    
                           
class Step04FormSensor(forms.Form):

    label = 'IPAddress:'

    title = '''What is the Hostname or IP address of  Sguil Server that this sensor connect to.'''

    snq4 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True)
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SGUIL_CLIENT_IPADDRESS'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
	
class Step05FormSensor(forms.Form):

    label = 'Username:'

    title = '''Enter the user name that can SSH Sguil server and execute sudo.'''

    snq5 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         validators=[validate_alnum])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SGUIL_CLIENT_USERNAME'}))
    #val = forms.CharField(widget=forms.HiddenInput(attrs={'value':''}))
    

class Step06FormSensor(forms.Form):

    label = 'Port:'

    title = '''What would you like to set PF__RING min__num__slots to?<br /><br />
The default is 4096.  For busy networks, you may want to increasethis to
a higher number like 65534.<br /><br />If you need to change this later,
you can modify /etc/modprobe.d/pf__ring.conf and reload the pf_ring module.'''

    snq6 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='4096',
                          validators=[validate_port])
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PF_RING_SLOTS'}))


class Step07FormSensor(forms.Form):

    choices = [('eth0', 'eth0'),
				('eth1', 'eth1')]

    label = 'Network interface(s):'

    title = '''Which network interface(s) should be monitored?<br /><br />
If you allowed Setup to configure /etc/network/interfaces,
your monitor interfaces are already selected.'''

    snq7 = forms.MultipleChoiceField(label=label, required=True,
                                    choices=choices,
                                    widget=forms.CheckboxSelectMultiple())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'INTERFACES'}))
									
	

class Step08FormSensor(forms.Form):

    label = 'Enable IDS Engine:'

    title = '''The IDS Engine (Snort/Suricata) listens on the interfaces<br />
specified on the previous screen and logs IDS alerts.<br /><br />
Would you like to enable the IDS Engine?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    snq8 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_ENGINE_ENABLED'}))

class Step09FormSensor(forms.Form):

    label = 'Number of IDS engine processes:'

    title = '''How many IDS engine processes would you like to run?<br /><br />
This is limited by the number of CPU cores on your system.<br /><br />
If you need to change this setting later, change IDS_LB_PROCS
in /etc/nsm/HOSTNAME-INTERFACE/sensor.conf'''
    
    choices = [(1, 1),
               (2, 2),
               (3, 3)]
	
    
    snq9 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'IDS_LB_PROCS'}))
    


class Step10FormSensor(forms.Form):

    label = 'Enable Bro:'

    title = '''Bro listens on the chosen interfaces and writes protocol logs.<br /><br />
Would you like to enable Bro?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    snq10 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'BRO_ENABLED'}))


class Step11FormSensor(forms.Form):

    label = 'Enable file extraction:'

    title = '''Bro can extract files (EXEs by default) from your network
traffic.<br /><br />If enabled, EXEs will be stored in
/nsm/bro/extracted/.<br />
Would you like to enable file extraction?<br />'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    snq11 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'EXTRACT_FILES'}))


class Step12FormSensor(forms.Form):
   
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
    snq12 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'BRO_LB_PROCS'}))


class Step13FormSensor(forms.Form):

    label = 'Enable full packet capture:'

    title = '''Full packet capture writes all monitored traffic to disk.<br /><br />
Full packet capture requires lots of disk space,<br />
but gives you lots of forensic capabilities<br />
and is therefore highly recommended!<br />
Would you like to enable full packet capture?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    snq13 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_ENABLED'}))

class Step14FormSensor(forms.Form):

    label = 'File size:'

    title = '''How big do you want your pcap files to be?<br /><br />
Please enter an integer in Megabytes (MB). The default is 150 MB.'''

    snq14 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='150',
                          validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_SIZE_CONFIRMED'}))

class Step15FormSensor(forms.Form):

    label = 'Enable mmap I/O:'

    title = '''netsniff-ng defaults to using scatter/gather pcap file I/O.<br /><br />
For higher performance, you can enable mmap I/O,
but this requires more RAM.<br />Would you like to enable mmap I/O?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    snq15 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_OPTIONS'}))
							
class Step16FormSensor(forms.Form):

    label = 'PCAP ring buffer size:'

    title = '''How large do you want your PCAP ring buffer?<br /><br />
Each monitoring interface will have the specified amount allocated from
RAM<br />so be sure your system has enough memory. In the case of 4 sensor
interfaces<br />and a specified ring buffer of 1GB, 4GB of total RAM will
be allocated for packet<br />buffering. For busy networks a ring buffer
of at least 256MB is recommended.<br /><br />
Please enter an integer in Megabytes (MB). The default is 64 MB.<br />
How large do you want your PCAP ring buffer?'''

    snq16 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='64',
                          validators=[validate_int_digit])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'PCAP_RING_SIZE'}))


class Step17FormSensor(forms.Form):

    label = '''Percent:'''

    title = '''At what percent of disk usage would you like to begin
purging old logs?<br /><br />
Please enter an integer between 10 and 100.  The default is 90.'''

    snq17 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='90',
                          validators=[validate_range_10_100])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'CRIT_DISK_USAGE'}))

class Step18FormSensor(forms.Form):

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

    choices = [('0', 'Yes'),
               ('1', 'No')]

    snq18 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'SALT'}))


class Step19FormSensor(forms.Form):

    label = 'Port:'

    title = '''Please specificity on which port sensor should sent logs stream
to Server - should be the same as it was set on server.<br /><br />
The default is 5043 tcp port.
Please use range: 1-65535 only.  '''

    snq19 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='5043',
                          validators=[validate_port])
    key = forms.CharField(widget=forms.HiddenInput(attrs={'value':'LOGSTASH_REDIS_PORT'}))

class Step20FormSensor(forms.Form):

    label = 'Would you like to continue?'

    title = '''Click Yes to make this change in file'''

    choices = [('0', 'Yes,Proceed with Change!'),
               ('1', 'No, Dont make any Change!')]

    snq20 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())
    



