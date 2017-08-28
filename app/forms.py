# -*- coding: utf-8 -*-

from socket import gethostname
from django import forms
from django.core.validators import validate_email
from app.validators import *
from app.cmd import LocalCommand


class EditorForm(forms.Form):

    form2edit = forms.CharField(label='', help_text='',
                                widget=forms.Textarea())


class Step01Form(forms.Form):

    label = 'Would you like to continue?'

    title = '''Welcome to Cyber Defence Setup!<br />
This program will allow you to configure
Cyber Defence on {}.'''.format(gethostname())

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q1 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())


class Step02Form(forms.Form):

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

    choices = [('Standalone', 'Standalone'),
               ('IndexNode', 'IndexNode'),
               ('Server', 'Server'),
               ('Sensor', 'Sensor')]

    q2 = forms.ChoiceField(label=label, required=True,
                           choices=choices, widget=forms.RadioSelect())


class Step03Form(forms.Form):

    label = 'Hostname/IP address:'

    title = '''What is the hostname or IP address of the Sguil server that
            this sensor should connect to?'''

    q3 = forms.CharField(label=label, max_length=255,
                         min_length=2, required=True)


class Step04Form(forms.Form):

    label = 'Username:'

    title = '''Please enter a username that can SSH
to the Sguil server and execute sudo.'''

    q4 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True)


class Step05Form(forms.Form):

    label = 'Username:'

    title = '''What would you like your Sguil username to be?<br />This will be
        used when logging into Sguil, Squert.<br />Please use alphanumeric
        characters only.'''

    q5 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         validators=[validate_alnum])


class Step06Form(forms.Form):

    label = 'Email:'

    title = '''What is your email address?<br />
This will be used when logging into Snorby. '''

    q6 = forms.CharField(label=label, max_length=255,
                         min_length=6, required=True,
                         validators=[validate_email])


class Step07Form(forms.Form):

    label1 = 'Password:'

    label2 = 'Confirm password:'

    title = '''What would you like to set your password to?<br />
Password must be at least 6 characters.
Please use alphanumeric characters only!<br />
This password will be used for Sguil, Squert, Snorby.<br />
Once you've logged into these interfaces using this initial password,
you can change it in Sguil and Snorby.'''

    q7a = forms.CharField(label=label1, max_length=255,
                          min_length=6, required=True,
                          widget=forms.PasswordInput,
                          validators=[validate_alnum])

    q7b = forms.CharField(label=label2, max_length=255,
                          min_length=6, required=True,
                          widget=forms.PasswordInput,
                          validators=[validate_alnum])

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('q7a')
        password2 = cleaned_data.get('q7b')
        if password1 != password2:
            raise forms.ValidationError('Passwords didn\'t match!')


class Step08Form(forms.Form):

    lc = LocalCommand()

    label = 'Memory in GB:'

    title = '''Please set up memory in GB for index node - on this server you
have free ~{}.<br />
Half of this value is deafult'''.format(lc.get_max_es_memory())

    q8 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         initial='{}'.format(int(lc.get_max_es_memory()) / 2),
                         validators=[validate_mem_gb])


class Step09Form(forms.Form):

    label = 'Days:'

    title = '''How many days of data do you want to keep in your Sguil
database?<br />
This includes things like IDS alerts.<br />
If you need to change this later, you can change DAYSTOKEEP in
/etc/nsm/securityonion.conf.<br />
Please enter an integer. The default is 30 days.'''

    q9 = forms.CharField(label=label, max_length=255,
                         min_length=1, required=True,
                         initial='30',
                         validators=[validate_int_digit])


class Step10Form(forms.Form):

    label = 'Days:'

    title = '''How many days of data do you want to repair
in your Sguil database?<br />
A daily cronjob stops Sguil, repairs the MySQL tables for
the last X days, and then starts Sguil back up.<br />
If you choose a higher value, Sguil will be down for longer.<br />
If you need to change this later, you can change DAYSTOREPAIR
in /etc/nsm/securityonion.conf.<br />
Please enter an integer. The default is 7 days.'''

    q10 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='7',
                          validators=[validate_int_digit])


class Step11Form(forms.Form):

    label = 'IDS Engine:'

    title = '''Suricata IDS Engine is only choise for now'''

    q11 = forms.BooleanField(label=label, required=True)


class Step12Form(forms.Form):

    label = 'IDF ruleset:'

    title = '''Which IDS ruleset would you like to use?'''

    choices = [('ETGPL', 'ETGPL'),
               ('ETPRO', 'ETPRO'),
               ('VRT', 'VRT'),
               ('VRTET', 'VRTET')]

    q12 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step13Form(forms.Form):

    label = 'Emerging Threats Pro oinkcode:'

    title = '''Please enter your Emerging Threats Pro oinkcode.<br /><br />
If you don't already have one, you can purchase one from
http://www.emergingthreatspro.com/.'''

    q13 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True)


class Step14Form(forms.Form):

    label = 'Snort VRT oinkcode:'

    title = '''Please enter your Snort VRT oinkcode.<br /><br />
If you don't already have one, you can obtain one from
http://www.snort.org/.'''

    q14 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True)


class Step15Form(forms.Form):

    label = 'VRT policy:'

    title = '''Please choose a VRT policy.'''

    choices = [('connectivity', 'connectivity'),
               ('balanced', 'balanced'),
               ('security', 'security')]

    q15 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step16Form(forms.Form):

    label = 'Port:'

    title = '''Please specificity on which server will receive
logs stream from Sensor.<br /><br /> The default is 5043 tcp port.
Please use range: 1-65535 only.'''

    q16 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='5043',
                          validators=[validate_port])


class Step17Form(forms.Form):

    lc = LocalCommand()

    label = 'Memory in GB:'

    title = '''Please set up memory in GB
for elasticsearch node - on this server you have
free ~{}.<br />
Half of this value is deafult'''.format(lc.get_max_es_memory())

    q17 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='{}'.format(int(lc.get_max_es_memory()) / 2),
                          validators=[validate_mem_gb])


class Step18Form(forms.Form):

    label = 'Port:'

    title = '''What would you like to set PF__RING min__num__slots to?<br /><br />
The default is 4096.  For busy networks, you may want to increasethis to
a higher number like 65534.<br /><br />If you need to change this later,
you can modify /etc/modprobe.d/pf__ring.conf and reload the pf_ring module.'''

    q18 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='4096',
                          validators=[validate_port])


class Step19Form(forms.Form):

    lc = LocalCommand()
    choices = lc.get_if_list()
    initval = lc.get_if_manual_list()

    label = 'Network interface(s):'

    title = '''Which network interface(s) should be monitored?<br /><br />
If you allowed Setup to configure /etc/network/interfaces,
your monitor interfaces are already selected.'''

    q19 = forms.MultipleChoiceField(label=label, required=True,
                                    choices=choices,
                                    initial=initval,
                                    widget=forms.CheckboxSelectMultiple())


class Step20Form(forms.Form):

    label = 'Enable IDS Engine:'

    title = '''The IDS Engine (Snort/Suricata) listens on the interfaces<br />
specified on the previous screen and logs IDS alerts.<br /><br />
Would you like to enable the IDS Engine?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q20 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step21Form(forms.Form):

    lc = LocalCommand()

    label = 'Number of IDS engine processes:'

    title = '''How many IDS engine processes would you like to run?<br /><br />
This is limited by the number of CPU cores on your system.<br /><br />
If you need to change this setting later, change IDS_LB_PROCS
in /etc/nsm/HOSTNAME-INTERFACE/sensor.conf'''

    q21 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial=lc.get_cpu_count() / 2,
                          validators=[validate_cpu])


class Step22Form(forms.Form):

    label = 'Enable Bro:'

    title = '''Bro listens on the chosen interfaces and writes protocol logs.<br /><br />
Would you like to enable Bro?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q22 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step23Form(forms.Form):

    label = 'Enable file extraction:'

    title = '''Bro can extract files (EXEs by default) from your network
traffic.<br /><br />If enabled, EXEs will be stored in
/nsm/bro/extracted/.<br />
Would you like to enable file extraction?<br />'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q23 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step24Form(forms.Form):

    lc = LocalCommand()

    label = 'Number of Bro processes:'

    title = '''How many Bro processes would you like to run?<br /><br />
This is limited by the total number of CPU cores on your system,<br />
but you should probably choose no more than HALF
your number of CPU cores.<br /><br />
If you need to change this setting later, you can change the lb_procs variable
in /opt/bro/etc/node.cfg.'''

    q24 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial=lc.get_cpu_count() / 2,
                          validators=[validate_cpu])


class Step25Form(forms.Form):

    label = 'Enable full packet capture:'

    title = '''Full packet capture writes all monitored traffic to disk.<br /><br />
Full packet capture requires lots of disk space,<br />
but gives you lots of forensic capabilities<br />
and is therefore highly recommended!<br />
Would you like to enable full packet capture?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q25 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step26Form(forms.Form):

    label = 'File size:'

    title = '''How big do you want your pcap files to be?<br /><br />
Please enter an integer in Megabytes (MB). The default is 150 MB.'''

    q26 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='150',
                          validators=[validate_int_digit])


class Step27Form(forms.Form):

    label = 'Enable mmap I/O:'

    title = '''netsniff-ng defaults to using scatter/gather pcap file I/O.<br /><br />
For higher performance, you can enable mmap I/O,
but this requires more RAM.<br />Would you like to enable mmap I/O?'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q27 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step28Form(forms.Form):

    label = 'PCAP ring buffer size:'

    title = '''How large do you want your PCAP ring buffer?<br /><br />
Each monitoring interface will have the specified amount allocated from
RAM<br />so be sure your system has enough memory. In the case of 4 sensor
interfaces<br />and a specified ring buffer of 1GB, 4GB of total RAM will
be allocated for packet<br />buffering. For busy networks a ring buffer
of at least 256MB is recommended.<br /><br />
Please enter an integer in Megabytes (MB). The default is 64 MB.<br />
How large do you want your PCAP ring buffer?'''

    q28 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='64',
                          validators=[validate_int_digit])


class Step29Form(forms.Form):

    label = '''Percent:'''

    title = '''At what percent of disk usage would you like to begin
purging old logs?<br /><br />
Please enter an integer between 10 and 100.  The default is 90.'''

    q29 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='90',
                          validators=[validate_range_10_100])


class Step30Form(forms.Form):

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

    q30 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step31Form(forms.Form):

    label = 'Port:'

    title = '''Please specificity on which port sensor should sent logs stream
to Server - should be the same as it was set on server.<br /><br />
The default is 5043 tcp port.
Please use range: 1-65535 only.  '''

    q31 = forms.CharField(label=label, max_length=255,
                          min_length=1, required=True,
                          initial='5043',
                          validators=[validate_port])


class Step32Form(forms.Form):

    label = 'Would you like to continue?'

    title = '''We're about to do the following:<br />
- Set the OS timezone to UTC.
- Delete any existing NSM data/configuration. <br />
$SERVER_CONFIRM
$SERVER_USER_CONFIRM
$SNORBY_USER_CONFIRM
$LOGSTASH_REDIS_CONFIRM
$ELASTICSEARCH_IP_CONFIRM
$SENSOR_CONFIRM_1
$SENSOR_CONFIRM_2
$SENSOR_CONFIRM_3
$IDS_LB_PROCS_CONFIRM
$BRO_LB_PROCS_CONFIRM
$IDS_RULESET_ACTION
$ES_NODE_CONFIRM

We're about to make changes to your system!'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q32 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())



class Step33Form(forms.Form):

    label = 'Would you like to continue?'

    title = '''We're about to do the following:<br />
- Set the OS timezone to UTC. <br />
- Delete any existing NSM data/configuration. <br />
$ES_NODE_CONFIRM
<br />
We're about to make changes to your system!'''

    choices = [('0', 'Yes'),
               ('1', 'No')]

    q33 = forms.ChoiceField(label=label, required=True,
                            choices=choices, widget=forms.RadioSelect())


class Step34Form(forms.Form):

    title = '''Setup is now complete! <br /> <br />
Setup log can be found here:<br />
/var/log/nsm/sosetup.log<br />
<br />
You may view IDS alerts using Sguil, Squert, Snorby, or Elasticsearch. <br />
<br />
Bro logs can be found in Elasticsearch and the following location: <br />
/nsm/bro/'''


class Step35Form(forms.Form):

    title = '''Rules downloaded by Pulledpork are stored in: <br />
/etc/nsm/rules/downloaded.rules <br />
<br />
Local rules can be added to: <br />
/etc/nsm/rules/local.rules <br />
<br />
You can have PulledPork modify the downloaded rules <br />
by modifying the files in: <br />
/etc/nsm/pulledpork/ <br />
<br />
Rules will be updated every day at 7:01 AM UTC. <br />
You can manually update them by running: <br />
/usr/bin/rule-update <br />
<br />
Sensors can be tuned by modifying the files in: <br />
/etc/nsm/NAME-OF-SENSOR/'''


class Step36Form(forms.Form):

    lc = LocalCommand()

    title = '''Setup is now complete! <br /> <br />
Setup log can be found here:<br />
/var/log/nsm/sosetup.log<br />
<br />
Index Node was added. You can run: <br />
curl -XGET 'http://{}:9200/_cluster/health?pretty=true'<br />
to check if node was added to cluster.'''.format(lc.get_ip_mgmt('eth0'))
