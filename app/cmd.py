# -*- coding: utf-8 -*-

from paramiko import SSHClient, AutoAddPolicy
from paramiko.util import log_to_file
from subprocess import check_output, call
from uuid import uuid4
from re import findall, compile

class LocalCommand():

    def read(self, path):
        # dodać sudo
        return check_output(['cat', path]).split()

    def write(self, data, path):
        self.tmp_path = '/tmp/tmp_file_{}'.format(uuid4())
        with open(path, mode='w') as f:
            f.write(data)
        # dodać sudo
        call(['cp', self.tmp_path, path])

    def get_if_list(self):
        if_list = []
        tmp = [findall(compile(r'^ *(eth.|bond.|wlan.|br.|ath.|bge.|mon.|fe.)'), l) for l in self.read('/proc/net/dev')]
        for i in tmp:
            if i:
                if_list.append((str(i[0]), str(i[0])))
        return if_list

    def get_if_manual_list(self):
        tmp = []
        for i in check_output(['awk', '/auto/ {print $2}', '/etc/network/interfaces']).split():
            tmp.append(str(i))
        return tmp

    def get_max_es_memory(self):
        return self.read('/proc/meminfo')[1][0]

    def get_cpu_count(self):
        from multiprocessing import cpu_count
        return cpu_count()
        return 0

    def get_ip_mgmt(self, interface):
        from socket import inet_aton
        try:
            ip = '0.0.0.0'
            #ip = check_output(['ifconfig', interface]).split('\n')[1].strip().split()[1]
            #inet_aton(address)
        except:
            ip = '0.0.0.0'
        return ip


class RemoteCommand():

    def __init__(self, name, port, user, password='', timeout=30):
        log_to_file('rc.log')
        self.name = name
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout
        self.input = None
        self.output = None
        self.error = None
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.tmp_path = '/tmp/tmp_file_{}'.format(uuid4())
        if not password:
            self.ssh.connect(hostname=self.name, port=self.port,
                             username=self.user, timeout=self.timeout)
        else:
            self.ssh.connect(hostname=self.name, port=self.port,
                             username=self.user, password=self.password,
                             timeout=self.timeout)

    def read(self, path):
        self.input = None
        self.output = None
        self.error = None
        # dodać sudo
        (self.input,
            self.output,
            self.error) = self.ssh.exec_command('cat {}'.format(path))
        # sftp = self.ssh.open_sftp()
        # file = sftp.open(path, 'r')
        # self.output = file.readlines()
        # file.close()

    def write(self, data, path):
        self.input = None
        self.output = None
        self.error = None
        sftp = self.ssh.open_sftp()
        file = sftp.open(self.tmp_path, 'w')
        tmp = ''
        for line in data.split('\n'):
            tmp += line.rstrip('\r')
            tmp += '\n'
        file.write(tmp)
        file.close()
        # dodać sudo
        (self.input,
            self.output,
            self.error) = self.ssh.exec_command('cp {} {}'.format(self.tmp_path, path))

    def service(self, name, cmd):
        self.input = None
        self.output = None
        self.error = None
        # dodać sudo
        (self.input,
            self.output,
            self.error) = self.ssh.exec_command('service {} {}'.format(name, cmd))
        # self.ssh.exec_command('systemctl {} {}'.format(cmd, name))

    def exec_cmd(self, cmd):
        self.input = None
        self.output = None
        self.error = None
        # dodać sudo
        (self.input,
            self.output,
            self.error) = self.ssh.exec_command('bash {}'.format(cmd))

    def close(self):
        self.input = None
        self.output = None
        self.error = None
        # dodać sudo
        (self.input,
            self.output,
            self.error) = self.ssh.exec_command('rm {}'.format(self.tmp_path))
        self.ssh.close()

    def connect(self):
        self.ssh.connect(hostname=self.name,
                         port=self.port, username=self.user)

    def get_input(self):
        tmp = ''
        for line in self.input:
            tmp += line
        return tmp

    def get_output(self):
        tmp = ''
        try:
            for line in self.output:
                tmp += line
        except:
            pass
        return tmp

    def get_error(self):
        tmp = ''
        try:
            for line in self.error:
                tmp += line
        except:
            pass
        return tmp
