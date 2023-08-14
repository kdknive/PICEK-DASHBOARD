# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, send_file, make_response
from flask_login import login_required
from jinja2 import TemplateNotFound
import json, csv
from apps import db
from apps.scraper.model.projects import Project
from apps.scraper.model.groups import Group
from apps.scraper.model.cbf import CBF
from apps.scraper.data_handler import insertDB
import pandas as pd

groupsPath = []
groups = []
projects = []


@blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    global groupsPath
    global groups
    global projects

    if request.method == 'POST' and request.headers.get('type') == 'path':
        groupsPath.append({'path': json.loads(request.data).get('path'), 'parentID': json.loads(request.data).get('parentID')})
        return render_template('home/components/path-list.html', groupsPath=groupsPath)
    
    if request.method == 'POST' and request.headers.get('type') == 'groupsFilter':
        groups = Group.query.filter(Group.parentID == json.loads(request.data).get('parentID')).order_by(Group.groupName.asc())
        return render_template('home/components/groups-filter.html', groups=groups)
    
    if request.method == 'GET' and request.headers.get('type') == 'projectsFilter':
        if groupsPath:
            page = request.args.get('page', 1, type=int)
            paths = [ paths['path'] for paths in groupsPath ]
            projects = Project.query.filter(Project.path.startswith('/'.join(paths) + '/')).paginate(page=page, per_page=10)
        else:
            page = request.args.get('page', 1, type=int)
            projects = Project.query.paginate(page=page, per_page=10)
        return render_template('home/components/projects-filter.html', projects=projects)
        
    if request.method == 'POST' and request.headers.get('type') == 'projectsSearch':
        if groupsPath:
            page = request.args.get('page', 1, type=int)
            paths = [ paths['path'] for paths in groupsPath ]
            projects = Project.query.filter(Project.path.startswith('/'.join(paths) + '/')).filter(Project.project.contains(json.loads(request.data).get('searchValue'))).paginate(page=page, per_page=10)
        else:
            page = request.args.get('page', 1, type=int)
            projects = Project.query.filter(Project.project.contains(json.loads(request.data).get('searchValue'))).paginate(page=page, per_page=10)
        return render_template('home/components/projects-filter.html', projects=projects)
    
    if request.method == 'POST' and request.headers.get('type') == 'page_num':
        page = int(json.loads(request.data).get('page_num'))
        searchForm = json.loads(request.data).get('searchForm')
        if groupsPath:
            paths = [ paths['path'] for paths in groupsPath ]
            if searchForm:
                projects = Project.query.filter(Project.path.startswith('/'.join(paths) + '/')).filter(Project.project.contains(searchForm)).paginate(page=page, per_page=10)
            else:
                projects = Project.query.filter(Project.path.startswith('/'.join(paths) + '/')).paginate(page=page, per_page=10)
        else:
            if searchForm:
                projects = Project.query.filter(Project.project.contains(searchForm)).paginate(page=page, per_page=10)
            else:
                projects = Project.query.paginate(page=page, per_page=10)
        return render_template('home/components/projects-filter.html', projects=projects)
    
    if request.method == 'POST' and request.headers.get('type') == 'pathJump':
        if json.loads(request.data).get('index'):
            groupsPath = groupsPath[:int(json.loads(request.data).get('index'))]
        else:
            groupsPath = []
        return render_template('home/components/path-list.html', groupsPath=groupsPath)
    
    if request.method == 'GET' and request.headers.get('type') == 'export':
        searchForm = request.headers.get('searchForm')
        if groupsPath:
            paths = [ paths['path'] for paths in groupsPath ]
            if searchForm:
                projects = Project.query.filter(Project.path.startswith('/'.join(paths) + '/')).filter(Project.project.contains(searchForm))
            else:
                projects = Project.query.filter(Project.path.startswith('/'.join(paths) + '/'))
        else:
            if searchForm:
                projects = Project.query.filter(Project.project.contains(searchForm))
            else:
                projects = Project.query.all()

        with open('picek.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerows(["Project Name", "Project Path"])
            for p in projects:
                csvwriter.writerow([p.project, p.path])
        response = make_response(send_file('../picek.csv', mimetype="text/csv", download_name='picek.csv', as_attachment=True))
        response.headers['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response

    page = request.args.get('page', 1, type=int)

    groupsPath = []

    groups = Group.query.filter(Group.parentID == None).order_by(Group.groupName.asc())

    projects = Project.query.paginate(page=page, per_page=10)

    return render_template('home/dashboard.html', segment='dashboard', projects=projects, groups=groups, groupsPath=groupsPath)

@blueprint.route('/cbf', methods=['GET', 'POST'])
def cbf():
    insertDB("cbf", CBF)
    page = request.args.get('page', 1, type=int)

    cbf = CBF.query.paginate(page=page, per_page=10)
    return render_template("home/cbf.html", segment="cbf", cbf=cbf)

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'dashboard'

        return segment

    except:
        return None
