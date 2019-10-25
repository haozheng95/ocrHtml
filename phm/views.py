#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yinhaozheng
@software: PyCharm
@file: views.py
@time: 2019-10-25 09:38
"""

__mtime__ = '2019-10-25'

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if request.method == "GET":
        return render(request, "phm_index.html")
    return HttpResponseRedirect("/phm_show/")


def show(request):
    return render(request, "phm_show.html")
