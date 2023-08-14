from apps import db
from .model.projects import Project
from .model.groups import Group
import time
import urllib.request, json, csv
from .checker import checkByJobs
from .jenkins_scraper import getAllJobs
from flask import jsonify
import base64

giturl = "http://10.6.85.34/api/v4/"
jenkinsJobsBCA = getAllJobs("bcajenkins")
jenkinsJobsPCF = getAllJobs("pcf")
jenkinsJobsPBS = getAllJobs("pbs")

def getNumPages(target, extra=""):
    try:
        request = urllib.request.Request( giturl + target + "?access_token=cWtSvYV1ztBct94Ge-31&per_page=100", headers={"x-total-pages":""})
        response = urllib.request.urlopen(request)
        numPages = int(response.info()["x-total-pages"])
        return numPages
    except:
        return 1

def updateProjects():
    excludes = ("Administrator/", "automationtesting/", "BANKR/", "BIT/", "Documentation/", "II-SLPPI/", "ITBS/", "lost-and-found/", "PAI-B/", "PCF_Platform/", "QA/", "QA_OPS/", "rpa-internalapp/", "script-gitlab/", "xas-automation/", "XASAutomationTesting/")
    numPages = getNumPages("projects")
    for i in range(numPages):
        getUrl = giturl + "projects?access_token=cWtSvYV1ztBct94Ge-31&per_page=100&page=" + str(i+1)
        with urllib.request.urlopen(getUrl) as getData:
            data = json.load(getData)
        for x in data:
            if not x["path_with_namespace"].startswith(excludes):
                checked = checkByJobs(x["path_with_namespace"], jenkinsJobsBCA, jenkinsJobsPBS, jenkinsJobsPCF)
                db.session.merge(Project(projectID=x["id"], project=x["path"], created=x["created_at"], updated=x["last_activity_at"], path=x["path_with_namespace"], exist=checked["exist"], environment=checked["environment"], url=checked["url"], new=checked["new"], parentID=x["namespace"]["id"], oldestJob=checked["oldestJob"], newestJob=checked["newestJob"]))
    db.session.commit()    
    query = dict_helper(Project.query.all())
    return query

def updateGroups():
    excludes = ("Administrator", "automationtesting", "BANKR", "BIT", "Documentation", "II-SLPPI", "ITBS", "lost-and-found", "PAI-B", "PCF_Platform", "QA", "QA_OPS", "rpa-internalapp", "script-gitlab", "xas-automation", "XASAutomationTesting")
    numPages = getNumPages("groups")
    for i in range(numPages):
        getUrl = giturl + "groups?access_token=cWtSvYV1ztBct94Ge-31&per_page=100&page=" + str(i+1)
        with urllib.request.urlopen(getUrl) as getData:
            data = json.load(getData)
        for x in data:
            if not x["path"] in excludes:
                db.session.merge(Group(groupID=x["id"], groupName=x["path"], created=x["created_at"], parentID=x["parent_id"]))
    db.session.commit()
    query = dict_helper(Group.query.all())
    return query

def getProjects():
    query = dict_helper(Project.query.all())
    return query

def getGroups():
    query = dict_helper(Group.query.all())
    return query

def searchByPath(paths):
    result = []
    notExist = []
    pathList = paths.split(',')
    for path in pathList:
        detail = {"Project": path, "Status": False}
        projectPath = path
        trimPath = ["http://bcagitlab/", "http://bcagitlab.intra.bca.co.id/", "http://10.6.85.34/", ".git"]
        for i in trimPath:
            projectPath = projectPath.replace(i, "")
        pathList = projectPath.split('/')
        numPages = getNumPages("search", "&scope=projects&search=" + pathList[-1])
        for i in range(numPages):
            getUrl = giturl + "search?scope=projects&search=" + pathList[-1] + "&access_token=cWtSvYV1ztBct94Ge-31&per_page=100&page=" + str(i+1)
            with urllib.request.urlopen(getUrl) as getData:
                data = json.load(getData)
            for x in data:
                if x["path_with_namespace"] == projectPath:
                    detail.update({"Project": path, "Status": True})
                    break
        result.append(detail)
    for x in result:
        if x["Status"] == False:
            notExist.append("Project " + x["Project"] + " is not found. ")
    if notExist:
        return jsonify({
                    'Result': notExist,
                    'Message': "Please check your project URLs and try again."
                }),404
    return jsonify({
                'Result': "All URLs are found.",
                'Message': "Proceed to the next step."
            }),200

def getPipelineYAML():
    finalResult = []
    numPages = getNumPages("projects/3724/repository/branches")
    for i in range(numPages):
        getUrl = giturl + "projects/3724/repository/branches?access_token=cWtSvYV1ztBct94Ge-31&per_page=100&page=" + str(i+1)
        with urllib.request.urlopen(getUrl) as getData:
            data = json.load(getData)
            for x in data:
                try: 
                    checkUrl = giturl + "/projects/3724/repository/files/pipeline.yml?access_token=cWtSvYV1ztBct94Ge-31&ref=" + x["name"]
                    with urllib.request.urlopen(checkUrl) as getFile:
                        file = json.load(getFile)
                        content = str(base64.b64decode(file["content"]))
                        if "openshift" in content or "ocp" in content:
                            finalResult.append(x["name"])
                            print(x["name"] + " is using Openshift")
                        else:
                            print(x["name"] + " is not using Openshift")
                except:
                    print(x["name"] + " Doesn't have a pipeline.yml")
    return finalResult
                        
def dict_helper(objlist):
    result2 = [item.serialize() for item in objlist]
    return result2
