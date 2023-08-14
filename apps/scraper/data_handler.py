from apps import db
import urllib.request, json
import os
import ssl
import pandas as pd

checkerURL=os.environ.get('checkerURL', 'http://localhost:5000')

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def insertDB(type, model):
    if type == "groups" or type == "projects":
        getUrl = checkerURL + "/read/" + type
        print("Getting all data...")
        with urllib.request.urlopen(getUrl, context=context) as getData:
            data = json.load(getData)
        print("Finished getting all data!")

        if type == "groups":
            for i in data["groups"]:
                db.session.merge(model(groupID=i["groupID"], groupName=i["groupName"], created=i["created"], parentID=i["parentID"]))
        if type == "projects":
            for i in data["projects"]:
                db.session.merge(model(projectID=i["projectID"], project=i["project"], created=i["created"], updated=i["updated"], path=i["path"], exist=i["exist"], environment=i["environment"], url=i["url"], new=i["new"], parentID=i["parentID"], oldestJob=i["oldestJob"], newestJob=i["newestJob"]))
    if type == "cbf":
        df = pd.read_excel('./apps/files/Review CI CD untuk Aplikasi Pendukung CBF 2022.xlsx', sheet_name=['(Updated) Status CI-CD'])
        fileDict = df['(Updated) Status CI-CD'].fillna(0).to_dict('records')
        for i in fileDict:
            db.session.merge(model(cbfName=i["Aplikasi Pendukung CBF"], biro=i["Biro"], platform=i["Platform (VM/OCP/PCF)"], repo=True if i["Repo Git (diisi oleh tim release)"] else False , pipeline=True if i["Job Pipeline (UAT. DEV, Master)"] else False, generate=True if i["Job Generate"] else False, approval=True if i["Job Approval"] else False, deploy=True if i["Deploy"] else False, restart=True if i["Restart"] else False, keterangan=i["Keterangan"] if i["Keterangan"] else None))
    db.session.commit()