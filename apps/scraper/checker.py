import json
import datetime

def checkByJobs(path, jenkinsJobsBCA, jenkinsJobsPBS, jenkinsJobsPCF):
    pathPBS = path.split("/")
    finalPath = ""
    data = {}
    jobNamesBCA = [d.get('job', None) for d in jenkinsJobsBCA]
    jobNamesPBS = [d.get('job', None) for d in jenkinsJobsPBS]
    jobNamesPCF = [d.get('job', None) for d in jenkinsJobsPCF]
    for k in range(len(pathPBS)):
            if k == 0:
                finalPath += pathPBS[0] + "/BUILD"
            else:
                finalPath += "/" + pathPBS[k]
    if any(test.startswith(path) for test in jobNamesBCA):
        url = "http://10.22.85.32:8080"
        urlPath = path.split("/")
        for k in urlPath:
            url += "/job/" + k
        jobTime = []
        for z in jenkinsJobsBCA:
            a = z.get('job', None)
            if a.startswith(path): 
                firstTime = z.get('firstBuildTime', None)
                if firstTime:
                    date_time_obj = datetime.datetime.strptime(firstTime, '%Y-%m-%dT%H:%M:%S+%f')
                    jobTime.append(date_time_obj)
                lastTime = z.get('lastBuildTime', None)
                if lastTime:
                    date_time_obj = datetime.datetime.strptime(lastTime, '%Y-%m-%dT%H:%M:%S+%f')
                    jobTime.append(date_time_obj)
        if (path + "/APPROVAL-MANAGER") in jobNamesBCA and (path + "/GENERATE") in jobNamesBCA and (path + "/PIPELINE") in jobNamesBCA:
            data = {
                "exist": True,
                "environment": "bcajenkins",
                "url": url,
                "new": True,
                "oldestJob": min(jobTime, default=None),
                "newestJob": max(jobTime, default=None)
            }
        else:
            data = {
                "exist": True,
                "environment": "bcajenkins",
                "url": url,
                "new": False,
                "oldestJob": min(jobTime, default=None),
                "newestJob": max(jobTime, default=None)
            }        
    elif any(test.startswith(finalPath) for test in jobNamesPBS):
        url = "http://10.38.85.33:8080"
        urlPath = path.split("/")
        for k in range(len(path)):
            if k == 0:
                url += "/job/" + path[0] + "/job/BUILD"
            else:
                url += "/job/" + path[k]
        jobTime = []
        for z in jenkinsJobsPBS:
            a = z.get('job', None)
            if a.startswith(finalPath):
                firstTime = z.get('firstBuildTime', None)
                if firstTime:
                    date_time_obj = datetime.datetime.strptime(firstTime, '%Y-%m-%dT%H:%M:%S+%f')
                    jobTime.append(date_time_obj)
                lastTime = z.get('lastBuildTime', None)
                if lastTime:
                    date_time_obj = datetime.datetime.strptime(lastTime, '%Y-%m-%dT%H:%M:%S+%f')
                    jobTime.append(date_time_obj)
        data = {
            "exist": True,
            "environment": "PBS",
            "url": url,
            "new": None,
            "oldestJob": min(jobTime, default=None),
            "newestJob": max(jobTime, default=None)
        }
    elif any(test.startswith(path) for test in jobNamesPCF):
        url = "http://10.6.85.41:8080"
        urlPath = path.split("/")
        for k in urlPath:
            url += "/job/" + k
        jobTime = []
        for z in jenkinsJobsPCF:
            a = z.get('job', None)
            if a.startswith(path):
                firstTime = z.get('firstBuildTime', None)
                if firstTime:
                    date_time_obj = datetime.datetime.strptime(firstTime, '%Y-%m-%dT%H:%M:%S+%f')
                    jobTime.append(date_time_obj)
                lastTime = z.get('lastBuildTime', None)
                if lastTime:
                    date_time_obj = datetime.datetime.strptime(lastTime, '%Y-%m-%dT%H:%M:%S+%f')
                    jobTime.append(date_time_obj)
        data = {
            "exist": True,
            "environment": "PCF",
            "url": url,
            "new": None,
            "oldestJob": min(jobTime, default=None),
            "newestJob": max(jobTime, default=None)
        }
    else:
        data = {
            "exist": False,
            "environment": "",
            "url": "",
            "new": None,
            "oldestJob": None,
            "newestJob": None
        }
    return data