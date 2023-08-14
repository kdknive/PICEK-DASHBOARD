import urllib.request, json
from urllib.parse import urlencode
from http.client import HTTPSConnection
from base64 import b64encode
from getpass import getpass
from os import path

def basicAuth(username, password):
  token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
  return f'Basic {token}'

def getHeaders(environment):
  file = open("credentials.json")
  creds = json.load(file)
  if environment == "bcajenkins":
    headers = { 'Authorization' : basicAuth(creds["uDomain"], creds["api-bcajenkins"]) }
  elif environment == "pcf":
    headers = { 'Authorization' : basicAuth(creds["jenkins-pcf"], creds["jenkins-pcf-password"]) }
  elif environment == "pbs":
    headers = { 'Authorization' : basicAuth(creds["uDomain"], creds["api-pbs"]) }
  return headers

def getAllJobs(environment):
  file = open("./scripts/getJenkinsJobsData.groovy")
  script = {"script": file.read()}
  if environment == "bcajenkins":
    request = urllib.request.Request("http://10.22.85.32:8080/scriptText", data=urlencode(script).encode("utf-8"), headers=getHeaders(environment), method='POST')
  elif environment == "pcf":
    request = urllib.request.Request("http://10.6.85.41:8080/scriptText", data=urlencode(script).encode("utf-8"), headers=getHeaders(environment), method='POST')
  elif environment == "pbs":
    request = urllib.request.Request("http://10.38.85.33:8080/scriptText", data=urlencode(script).encode("utf-8"), headers=getHeaders(environment), method='POST')
  response = urllib.request.urlopen(request)
  stringResponse = str(response.read().decode("utf-8"))
  jsonResponse = json.loads(stringResponse)
  return jsonResponse