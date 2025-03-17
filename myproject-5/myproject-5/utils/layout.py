#!/usr/bin/python
# -*- coding: UTF-8 -*-



from flask import render_template,request,jsonify


def layout(template_name_or_list,**context):
    return render_template(template_name_or_list,
                           tag = request.url.split('/')[-2],
                           **context)


def outputnJsoByMessage(isSuccess,message):
    dict = {}
    dict['isSuccess'] = isSuccess if isSuccess else 0
    dict['message'] = isSuccess if isSuccess else ' '
    return jsonify(dict)

