# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from re import compile, sub
from app.cmd import LocalCommand


def validate_alnum(value):
    if value != sub(compile('[\W_]+'), '', value):
        raise ValidationError('Please use alphanumeric characters only.')

def validate_int_digit(value):
    lc = LocalCommand()
    mes = lc.get_max_es_memory()

    if not str(value).isdigit() or not int(value):
        raise ValidationError('''Please use integers only.''')

def validate_mem_gb(value):
    lc = LocalCommand()
    mes = lc.get_max_es_memory()

    if not str(value).isdigit() or int(value) >= mes:
        raise ValidationError('''Invalid memory! Please use integers less than
{}.'''.format(mes))

def validate_port(value):
    if not str(value).isdigit() or int(value) < 1 or int(value) > 65535:
        raise ValidationError('''Please use integers between 1-65535.''')

def validate_cpu(value):
    lc = LocalCommand()
    cores = lc.get_cpu_count()
    if not str(value).isdigit() or int(value) < 1 or int(value) > cores:
        raise ValidationError('''Please use integers between
1-{}.'''.format(cores))

def validate_range_10_100(value):
    if not str(value).isdigit() or int(value) < 10 or int(value) > 100:
        raise ValidationError('''Please use integers between 10 and 100.''')
