#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:    toddlerya
# @Date:      2018/6/9 18:41
# @FileName:  conf.py.py

from __future__ import unicode_literals

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'json_db': {
        'NAME': os.path.join(os.path.join(BASE_DIR, 'database'), 'db.json'),
    }
}

