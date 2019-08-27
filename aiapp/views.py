#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yinhaozheng
@software: PyCharm
@file: view.py
@time: 2019-08-21 10:28
"""
import hashlib
import os
import time

import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pdf2image import convert_from_path

from aiapp.chinese_ocr.export import export

__mtime__ = '2019-08-21'

my_path = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(os.path.dirname(my_path), "static")
save_path = os.path.join(static_path, "taskFiles")
down_path = os.path.join(static_path, "downFiles")
image_path = os.path.join(static_path, "imageFiles")
result_path = os.path.join(static_path, "resultFiles")
record_path = os.path.join(static_path, "record")
form_file_name = "exampleInputFile"


def index(request):
    if request.method == "GET":
        return render(request, "hello.html")

    task_file = upload_file(request)
    hl = hashlib.md5()
    hl.update(task_file.encode(encoding='utf-8'))
    task_id = hl.hexdigest()
    record = process(task_file, task_id)
    with open(os.path.join(record_path, task_id), "w", encoding="utf-8") as f:
        json.dump(record, f)
    return HttpResponseRedirect("/show/" + task_id)


def show(request, task_id):
    record = read_record(task_id)
    data = []
    for row in record:
        img = row["source"].replace(static_path, "/static")
        print(img)
        content = read_task_file(row["target"])
        data.append(
            dict(img=img, content=content)
        )
    return render(request, "show.html", dict(data=data, task_id=task_id))


def upload_file(request):
    file_name = str(time.time()) + "__" + request.FILES[form_file_name].name
    task_path = os.path.join(save_path, file_name)
    handle_uploaded_file(request.FILES[form_file_name].file, task_path)
    return file_name


def process(task_file, task_id):
    source_path = os.path.join(save_path, task_file)
    source_paths = []
    if task_file[-3::].lower() == "pdf":
        raw = source_path[:-4]
        pages = convert_from_path(source_path)
        for i in range(0, len(pages)):
            source_path = raw + str(i) + '.jpeg'
            source_paths.append(source_path)
            pages[i].save(source_path, 'jpeg')

    i = 0
    model_list = []
    for source_path in source_paths:
        target = task_id + str(i)
        export(source_path, result_path,
               os.path.join(down_path, target))
        i += 1
        model_list.append(dict(source=source_path, target=target))
    return model_list


def download(request, task_id):
    target = os.path.join(down_path, task_id)
    if not os.path.exists(target):
        record = read_record(task_id)
        with open(target, "wb+") as file:
            for row in record:
                target_id = row["target"]
                path = os.path.join(down_path, target_id)
                with open(path, "rb") as f:
                    for j in f:
                        file.write(j)

    with open(target, 'rb') as file:
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % task_id + ".txt"
    return response


def read_record(task_id):
    file = os.path.join(record_path, task_id)
    with open(file, "r", encoding="utf-8") as f:
        record = json.load(f)

    return record


def read_task_file(task_id):
    result = ""
    with open(os.path.join(down_path, task_id), 'r', encoding="utf-8") as file:
        for row in file:
            result += row
    return result


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f:
            destination.write(chunk)
