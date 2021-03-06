from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app.views import ConfigWizard
import os.path

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', auth_views.login),
    url(r'^dashboard/$', 'app.views.dashboard'),
    url(r'^config/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^pwc/$', auth_views.password_change),
    url(r'^service(?P<path_name>.*)\/$', 'app.views.service'),
    url(r'^file(?P<path_name>.*)\/$', 'app.views.file'),
    url(r'^script(?P<path_name>.*)\/$', 'app.views.script'),
    url(r'^server/$', 'app.views.config_server_wizard'),
    url(r'^sensor/$', 'app.views.config_sensor_wizard'),
    url(r'^standalone/$', 'app.views.config_standalone_wizard'),
    url(r'^indexnode/$', 'app.views.config_indexnode_wizard'),
    url(r'^wizard/$', 'app.views.login_required_wizard'),
    url(r'^viewjobs/$', 'app.views.view_jobs'),
    url(r'^viewjobdetails/$', 'app.views.view_job_details'),
    url(r'^startjob/$', 'app.views.start_job'),
    # url(r'^wizard/$', ConfigWizard.as_view([Step1Form, Step2Form])),
    # url(r'^network/$', 'app.views.network'),
    # url(r'^$', include(app.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/static/'}),
)
