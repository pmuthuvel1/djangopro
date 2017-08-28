# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from app.models import FileList, ServerConf, NetworkConf
from app.forms import *
from app.serverforms import *
from app.cmd import LocalCommand, RemoteCommand
import subprocess
import traceback
import sys
import os
from io import StringIO
import logging
from django.core.files import File
import os.path
from app.sensorforms import *
from app.standaloneforms import *
from app.indexnodeforms import *

from django.http import HttpResponseRedirect, HttpResponse
from models import MachineDetail, LoginDetail,ConfigType,ConfigPath,ScriptPath

import paramiko


import pxssh

logger = logging.getLogger("app")

FORMS = [#('step00form', Step00Form),
         ('step01form', Step01Form),
         ('step02form', Step02Form),
         ('step03form', Step03Form),
         ('step04form', Step04Form),
         ('step05form', Step05Form),
         ('step06form', Step06Form),
         ('step07form', Step07Form),
         ('step08form', Step08Form),
         ('step09form', Step09Form),
         ('step10form', Step10Form),
         ('step11form', Step11Form),
         ('step12form', Step12Form),
         ('step13form', Step13Form),
         ('step14form', Step14Form),
         ('step15form', Step15Form),
         ('step16form', Step16Form),
         ('step17form', Step17Form),
         ('step18form', Step18Form),
         ('step19form', Step19Form),
         ('step20form', Step20Form),
         ('step21form', Step21Form),
         ('step22form', Step22Form),
         ('step23form', Step23Form),
         ('step24form', Step24Form),
         ('step25form', Step25Form),
         ('step26form', Step26Form),
         ('step27form', Step27Form),
         ('step28form', Step28Form),
         ('step29form', Step29Form),
         ('step30form', Step30Form),
         ('step31form', Step31Form),
         ('step32form', Step32Form),
         ('step33form', Step33Form),
         ('step34form', Step34Form),
         ('step35form', Step35Form),
         ('step36form', Step36Form)]


SERVER_FORMS = [
         ('step01FormServer', Step01FormServer),
         ('step02formServer', Step02FormServer),
         ('step03formServer', Step03FormServer),
         ('step04formServer', Step04FormServer),
         ('step05formServer', Step05FormServer),
         ('step06formServer', Step06FormServer),
         ('step07formServer', Step07FormServer),
         ('step08formServer', Step08FormServer),
         ('step09formServer', Step09FormServer),
         ('step10formServer', Step10FormServer),
         ('step11formServer', Step11FormServer),
         ('step12formServer', Step12FormServer),
         ('step13formServer', Step13FormServer),
         ('step14formServer', Step14FormServer)]

SENSOR_FORMS = [
         ('step01FormSensor', Step01FormSensor),
         ('step02FormSensor', Step02FormSensor),
         ('step03FormSensor', Step03FormSensor),
         ('step04FormSensor', Step04FormSensor),
         ('step05FormSensor', Step05FormSensor),
         ('step06FormSensor', Step06FormSensor),
         ('step07formSensor', Step07FormSensor),
         ('step08formSensor', Step08FormSensor),
         ('step09formSensor', Step09FormSensor),
         ('step10formSensor', Step10FormSensor),
         ('step11formSensor', Step11FormSensor),
         ('step12formSensor', Step12FormSensor),
         ('step13formSensor', Step13FormSensor),
         ('step14formSensor', Step14FormSensor),
         ('step15formSensor', Step15FormSensor),
         ('step16formSensor', Step16FormSensor),
         ('step17formSensor', Step17FormSensor),
         ('step18formSensor', Step18FormSensor),
         ('step19formSensor', Step19FormSensor),
         ('step20formSensor', Step20FormSensor)]


STANDALONE_FORMS = [
         ('step01formStandalone', Step01FormStandalone),
         ('step02formStandalone', Step02FormStandalone),
         ('step03formStandalone', Step03FormStandalone),
         ('step04formStandalone', Step04FormStandalone),
         ('step05formStandalone', Step05FormStandalone),
         ('step06formStandalone', Step06FormStandalone),
         ('step07formStandalone', Step07FormStandalone),
         ('step08formStandalone', Step08FormStandalone),
         ('step09formStandalone', Step09FormStandalone),
         ('step10formStandalone', Step10FormStandalone),
         ('step11formStandalone', Step11FormStandalone),
         ('step12formStandalone', Step12FormStandalone),
         ('step13formStandalone', Step13FormStandalone),
         ('step14formStandalone', Step14FormStandalone),
         ('step15formStandalone', Step15FormStandalone),
         ('step16formStandalone', Step16FormStandalone),
         ('step17formStandalone', Step17FormStandalone),
         ('step18formStandalone', Step18FormStandalone),
         ('step19formStandalone', Step19FormStandalone),
         ('step20formStandalone', Step20FormStandalone),
         ('step21formStandalone', Step21FormStandalone),
         ('step22formStandalone', Step22FormStandalone),
         ('step23formStandalone', Step23FormStandalone),
         ('step24formStandalone', Step24FormStandalone),
         ('step25formStandalone', Step25FormStandalone),
         ('step26formStandalone', Step26FormStandalone)]

INDEXNODE_FORMS = [
         ('Step01formIndexNode', Step01FormIndexNode),
         ('Step02formIndexNode', Step02FormIndexNode),
         ('Step03formIndexNode', Step03FormIndexNode),
         ('Step04formIndexNode', Step04FormIndexNode),
         ('Step05formIndexNode', Step05FormIndexNode)]


class ConfigWizard(SessionWizardView):

    template_name = 'app/wizard.html'

    def done(self, form_list, **kwargs):
        return render_to_response('app/wizard_done.html', {
            'form_data': [form.cleaned_data for form in form_list]})


config_wizard_view = ConfigWizard.as_view(FORMS)


@login_required()
def login_required_wizard(request):
        return config_wizard_view(request)


class ConfigServerWizard(SessionWizardView):
    template_name = 'app/server.html'
    def done(self, form_list, **kwargs):
        #createServerFile(form_list)  
        filepath='/tmp/cdanswers'
        prefix='sq'
        keyval_list = createServerFile(self, form_list,filepath,prefix, **kwargs)
        return render_to_response('app/server_wizard_done.html', {
        'keyval_list': keyval_list,
        'filepath':filepath,
        'config_type':'Server'})

config_server_view = ConfigServerWizard.as_view(SERVER_FORMS)

@login_required()
def config_server_wizard(request):
        return config_server_view(request)
            
class ConfigSensorWizard(SessionWizardView):
    template_name = 'app/sensor.html'
    def done(self, form_list, **kwargs):
        #createServerFile(form_list)  
        filepath='/tmp/sensor_answers'
        prefix='snq'
        keyval_list = createServerFile(self, form_list,filepath,prefix, **kwargs)
        return render_to_response('app/server_wizard_done.html', {
        'keyval_list': keyval_list,
        'filepath':filepath,
        'config_type':'Sensor' })
               

config_sensor_view = ConfigSensorWizard.as_view(SENSOR_FORMS)

@login_required()
def config_sensor_wizard(request):
        return config_sensor_view(request)
    
class ConfigStandaloneWizard(SessionWizardView):
    template_name = 'app/standalone.html'
    def done(self, form_list, **kwargs):
        #createServerFile(form_list)  
        filepath='/tmp/standalone_answers'
        prefix='saq'
        keyval_list = createServerFile(self, form_list,filepath,prefix, **kwargs)
        return render_to_response('app/server_wizard_done.html', {
        'keyval_list': keyval_list,
        'filepath':filepath,
        'config_type':'Standalone' })
        
config_standalone_view = ConfigStandaloneWizard.as_view(STANDALONE_FORMS)

@login_required()
def config_standalone_wizard(request):
        return config_standalone_view(request)

    
class ConfigIndexNodeWizard(SessionWizardView):
    template_name = 'app/indexnode.html'
    def done(self, form_list, **kwargs):
        #createServerFile(form_list)  
        filepath='/tmp/indexnode_answers'
        prefix='inq'
        keyval_list = createServerFile(self, form_list,filepath,prefix, **kwargs)
        return render_to_response('app/server_wizard_done.html', {
        'keyval_list': keyval_list,
        'filepath':filepath,
        'config_type':'Indexnode' })
        
config_indexnode_view = ConfigIndexNodeWizard.as_view(INDEXNODE_FORMS)

@login_required()
def config_indexnode_wizard(request):
        return config_indexnode_view(request)



def createServerFile(self, form_list, filepath, prefix,**kwargs):
    keyval_list = []
    i=0
    with open(filepath, 'w+') as f:
        os.utime(filepath, None)
        myfile = File(f)
        for form in form_list:
            data = form.cleaned_data
            logger.info('data='+str(data))
            i+=1
            valname= prefix+str(i)
            try:
                if data.has_key('key'):
                #if 'key' in data:
                    line_value = str(data['key'])+"="+str(data[str(valname)])
                    myfile.writelines(line_value+"\n")
                    keyval_list.append(line_value)
            except:
                line_value = "dummy=dummy"
                myfile.writelines(line_value+"\n")
                keyval_list.append(line_value)                
        myfile.closed
        f.closed 
    return keyval_list;
    
        
@login_required()
def logout(request):

    request.session.flush()
    return render(request, 'app/logout.html', {'msg': 'Logout'})


@login_required()
def dashboard(request):

    server_list = list(ServerConf.objects.all())
    servers = {}
    msg = ''
    try:
        if request.session['msg']:
            msg = request.session['msg']
    except:
        pass
    rc = None
    try:
        nc_list = list(NetworkConf.objects.all())
        if len(nc_list) < 1:
            return redirect('/config/app/networkconf/add/')
    except:
        pass
    if len(server_list) < 1:
        return render(request, 'app/dashboard.html', {
            'msg': 'No servers on the server list'})
    for server in server_list:
        try:
            if server.password:
                rc = RemoteCommand(server.name, int(server.port),
                                   server.user, server.password)
                msg += '{}: password<br />'.format(server.name)
            else:
                rc = RemoteCommand(server.name, int(server.port), server.user)
                msg += '{}: keys<br />'.format(server.name)
            service_dict = {}
            for service in server.service_list.all():
                tmp = ''
                rc.service(service.name, 'status')
                err = rc.get_output()
                out = rc.get_error()
                if err or out:
                    tmp += out
                    tmp += err
                else:
                    tmp = 'Output/Error!'
                service_dict[service.name] = tmp
            servers[server] = service_dict
        except Exception as ex:
            msg += '{}: {}'.format(server.name, str(ex))
    return render(request, 'app/dashboard.html', {
        'servers': servers,
        'msg': msg})


@login_required()
def service(request, path_name):

    full_path = request.get_full_path()
    server_name = full_path.split('/service/')[1].split('/')[0]
    service_name = full_path.split('/service/')[1].split('/')[1]
    cmd = full_path.split('/service/')[1].split('/')[2]
    server = ServerConf.objects.get(name=server_name)
    msg = ''
    rc = None
    try:
        if server.password:
            rc = RemoteCommand(server.name, int(server.port),
                               server.user, server.password)
            msg += '{}: password<br />'.format(server.name)
        else:
            rc = RemoteCommand(server.name, int(server.port),
                               server.user)
            msg += '{}: keys<br />'.format(server.name)
    except Exception as ex:
        msg += '{}: {}'.format(server.name, str(ex))
    rc.service(service_name, cmd)
    # sprawdzenie czy plik istnieje w konfiguracji serwera !!!
    if rc.get_error():
        msg += '{}: {}<br />'.format(server.name, rc.get_output())
    else:
        msg += '{}: {}<br />'.format(server.name, rc.get_error())
    for service in server.service_list.all():
        rc.service(service.name, 'status')
        service.status = rc.get_error()
        service.status += rc.get_output()
    request.session['msg'] = msg
    return redirect('/dashboard/')


@login_required()
def file(request, path_name):

    msg = ''
    if len(request.get_full_path().split('/file/')[1].split('/')) < 3:
        msg += 'File does not exist.'
        return render(request, 'app/dashboard.html', {'msg': msg})
    server_name = request.get_full_path().split('/file/')[1].split('/')[0]
    server = ServerConf.objects.get(name=server_name)
    path = request.get_full_path().split(server_name)[1][:-1]
    msg = ''
    formd = None
    data = ''
    rc = None
    try:
        if server.password:
            rc = RemoteCommand(server.name, int(server.port),
                               server.user, server.password)
            msg += '{}: password<br />'.format(server.name)
        else:
            rc = RemoteCommand(server.name, int(server.port), server.user)
            msg += '{}: keys<br />'.format(server.name)
        rc.read(path)
        data = rc.get_output()
        print(data)
        tmp = request.POST.get('form2edit')
        if data != tmp and tmp is not None:
            data = tmp
            if str(data)[-2:] != '\r\n':
                data += '\r\n'
            rc.write(data, path)
            msg += '{}: {} saved.'.format(server.name, path)
        # sprawdzenie czy plik istnieje w konfiguracji serwera !!!
    except Exception as ex:
        msg += '{}: {}'.format(server.name, str(ex))
    formd = EditorForm(initial={'form2edit': data})
    return render(request, 'app/file.html', {'formd': formd,
                  'server': server, 'path': path, 'msg': msg})


@login_required()
def script(request, path_name):

    server_name = request.get_full_path().split('/script/')[1].split('/')[0]
    server = ServerConf.objects.get(name=server_name)
    path = request.get_full_path().split(server_name)[1][:-1]
    msg = ''
    formd = None
    data = ''
    rc = None
    output = ''
    try:
        if server.password:
            rc = RemoteCommand(server.name, int(server.port),
                               server.user, server.password)
            msg += '{}: password<br />'.format(server.name)
        else:
            rc = RemoteCommand(server.name, int(server.port), server.user)
            msg += '{}: keys<br />'.format(server.name)
        rc.read(path)
        data = rc.get_output()
        print(data)
        tmp = request.POST.get('form2edit')
        if data != tmp and tmp is not None:
            data = tmp
            rc.write(data, path)
            rc.exec_cmd(path)
            output = rc.get_error()
            output += rc.get_output()
            msg += '{}: {} saved & run.'.format(server.name, path)
        # sprawdzenie czy plik istnieje w konfiguracji serwera !!!
    except Exception as ex:
        msg += '{}: {}'.format(server.name, str(ex))
    formd = EditorForm(initial={'form2edit': data})
    return render(request, 'app/script.html',
                  {'formd': formd, 'server': server, 'path': path,
                   'msg': msg, 'output': output})




class ConfigTypeForm(forms.Form):
    cts = forms.ModelChoiceField(queryset=ConfigType.objects.all())


    
@login_required()
def view_jobs_old(request):
    """
    form = ConfigTypeForm()
    if request.method == "POST":
        form = ConfigTypeForm(request.POST)
        if form.is_valid:
            #redirect to the url where you'll process the input
            return HttpResponseRedirect('app/view_jobs.html') # insert reverse or url
    else:
        errors = form.errors or None # form not submitted or it has errors
    
        return render(request, 'app/view_jobs.html',{
          'form': form,
          'errors': errors,
          })
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConfigTypeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data['cts'])

            cts_value = form.cleaned_data['cts']
            
            if cts_value is not None :                
                return HttpResponseRedirect('/viewjobdetails/?ct='+str(cts_value))
            else:    
            # redirect to a new URL:
                return HttpResponseRedirect('/viewjobdetails/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConfigTypeForm()

    return render(request, 'app/view_jobs.html', {'form': form})
    #return render(request, 'app/view_jobs.html', {'ConfigTypes': ConfigType.objects.all()})

@login_required()
def view_job_details_old(request):
    print(request.GET['ct'])
    configType = ConfigType.objects.get(config_name=request.GET['ct'])
    print(configType)
    return render(request, 'app/view_job_details.html', {'configType': configType } )


   
class MachineDetaiForm(forms.Form):
    cts = forms.ModelChoiceField(queryset=MachineDetail.objects.all())   

@login_required()
def view_jobs(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MachineDetaiForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data['cts'])

            cts_value = form.cleaned_data['cts']
            
            if cts_value is not None :                
                return HttpResponseRedirect('/viewjobdetails/?ct='+str(cts_value))
            else:    
            # redirect to a new URL:
                return HttpResponseRedirect('/viewjobdetails/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MachineDetaiForm()

    return render(request, 'app/view_jobs.html', {'form': form})
    #return render(request, 'app/view_jobs.html', {'ConfigTypes': ConfigType.objects.all()})

@login_required()
def view_job_details(request):
    print(request.GET['ct'])
    machineDetail = MachineDetail.objects.get(ipaddress=request.GET['ct'])
    print(machineDetail)
    return render(request, 'app/view_job_details.html', {'machineDetail': machineDetail } )

@login_required()
def start_job(request):
    ipAdd = request.POST.get('ct')
    operation = request.POST.get('operation')
    print("ipAdd="+ipAdd)
    print("operation="+operation)
    mt = MachineDetail.objects.get(pk=ipAdd)
    if mt is None:
        return render(request, 'app/jobs_start_error.html', {'msg': 'Please configure a Remote Machine Details ' } )
    else:            
        print(mt.ipaddress+' '+mt.username+' '+mt.password)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(mt.ipaddress, username=mt.username, password=mt.password)
        
        jobstostart = request.POST.getlist('jobstostart')

        for x in jobstostart:
            print("jobstostart pk="+x)
            cpo = ScriptPath.objects.get(pk=x)
            print("sudo sh "+cpo.dirpath+cpo.scriptname)
            stdin, stdout, stderr = ssh.exec_command("sudo sh "+cpo.dirpath+cpo.scriptname)
            #print("stdout="+stdout.readlines())
            output = stdout.read()
            print "stdout",stdout.readlines()
                        
            print("output="+output)

            if len(output) > 99:
                output = output[0:99] 
   
            cpo.remarks= output 
    
            if operation == 'start':
                cpo.status = 'started'
            else:
                cpo.status = 'stopped'  
                
            cpo.save()
                
        #return render(request, 'app/view_job_details.html', {'machineDetail': mt } )
        return HttpResponseRedirect('/viewjobdetails/?ct='+str(ipAdd))
