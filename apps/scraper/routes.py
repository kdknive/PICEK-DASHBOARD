# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.scraper import blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import json
from .gitlab_scraper import updateProjects, updateGroups, getProjects, getGroups


@blueprint.route('/api/<object>', methods=['GET', 'POST'])
def api(object):
    if object == "projects":
        if request.method == "GET":
            return jsonify({
                    # 'error': '',
                    'projects': getProjects(),
                    'msg': 'Success scraping all projects from Gitlab!👍😀'
                })
        if request.method == "POST":
            return jsonify({
                    # 'error': '',
                    'projects': updateProjects(),
                    'msg': 'Success scraping all projects from Gitlab!👍😀'
                })
    elif object == "groups":
        if request.method == "GET":
            return jsonify({
                    # 'error': '',
                    'projects': getGroups(),
                    'msg': 'Success scraping all projects from Gitlab!👍😀'
                })
        if request.method == "POST":
            return jsonify({
                    # 'error': '',
                    'projects': updateGroups(),
                    'msg': 'Success scraping all projects from Gitlab!👍😀'
                })