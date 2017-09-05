#!/bin/python2.7

# Copyrights (c) Sec4You Consulting.

import requests
import yaml
from time import sleep
from os import getenv

class GrafanaManager(object):
  def __init__(self, server, port):
    self.server = server
    self.port = port
    self.proxies = False

    self.zbx_user = ""
    self.zbx_pswd = ""
    self.zbx_url = ""

    self.oim_server = str(getenv('OIM_SERVER'))

  def Login(self,username,password):
    if not self.proxies:
    	self.login = requests.post("http://localhost:3000/login",json={"user":username,"email":" ","password":password})
    else:
    	self.login = requests.post("http://localhost:3000/login",json={"user":username,"email":" ","password":password},proxies=self.proxies)
    self.cookie = self.login.headers['Set-Cookie'].split(";")
    self.token = ""
    del self.cookie[0]
    for i in self.cookie:
	    if "grafana_sess" in i:
		    grafana_sess = "{};".format(i.split(",")[1])
	    if "grafana_user" in i:
		    grafana_user = "{};".format(i.split(",")[1])
	    if "grafana_remember" in i:
		    grafana_remember = "{}".format(i.split(",")[1])
    self.token = grafana_sess + grafana_user + grafana_remember
    self.token=self.token.strip(" ").strip("\n")

  def EnablePlugin(self,plugin):
    hds = {'Referer':'http://{}:{}/plugins/{}/edit'.format(self.server,self.port,plugin),'Cookie':self.token, 'Accept':'application/json, text/plain, */*', 'X-Grafana-Org-Id':'1', 'Content-Type':'application/json;charset=utf-8','DNT':'1' }
    jdata = '{"enabled":true,"pinned":true,"jsonData":null}'
    jdata = yaml.load(jdata)
    if not self.proxies:
    	enable = requests.post("http://{}:{}/api/plugins/{}/settings".format(self.server,self.port,plugin),json=jdata,headers=hds)
    else:
    	enable = requests.post("http://{}:{}/api/plugins/{}/settings".format(self.server,self.port,plugin),json=jdata,headers=hds, proxies=self.proxies)
    print enable.text

  def CreateDatastore(self,datastore):
    #Datastores supported:
    # - zabbix
    hds = {'Referer':'http://{}:{}/datasources/new?gettingstarted'.format(self.server,self.port),'Cookie':self.token, 'Accept':'application/json, text/plain, */*', 'X-Grafana-Org-Id':'1', 'Content-Type':'application/json;charset=utf-8','DNT':'1' }
    if datastore == "Zabbix":
      jdata = '{{"name":"Zabbix","type":"alexanderzobnin-zabbix-datasource","url":"{}","access":"direct","jsonData":{{"dbConnection":{{"enable":false}},"username":"{}","password":"{}"}},"secureJsonFields":{{}},"isDefault":true}}'.format(self.zbx_url,self.zbx_user,self.zbx_pswd)
      jdata = yaml.load(jdata)
    if not self.proxies:
      enable = requests.post("http://{}:{}/api/datasources".format(self.server,self.port),json=jdata,headers=hds)
    else:
      enable = requests.post("http://{}:{}/api/datasources".format(self.server,self.port),json=jdata,headers=hds, proxies=self.proxies)
    print enable.text

  def ImportDashboard(self,dashboard):
    #Not working yet.
    #Templates at directory: grafana_dashboards
    hds = {'Accept':'application/json', 'Content-Type':'application/json;charset=utf-8','Cookie':self.token}
    dash = '{"dashboard":'+ open(dashboard,"r").read() + '}'
    if self.oim_server:
      dash.replace("<SERVER>",self.oim_server)
    jdata = yaml.load(dash)
    #print dashboard
    if not self.proxies:
      enable = requests.post("http://{}:{}/api/dashboards/db".format(self.server,self.port),json=jdata,headers=hds)
    else:
      enable = requests.post("http://{}:{}/api/dashboards/db".format(self.server,self.port),json=jdata,headers=hds, proxies=self.proxies)
    print enable.text


  def DeleteDashboard(self, dashboard):
    hds = {'Accept':'application/json', 'Content-Type':'application/json;charset=utf-8','Cookie':self.token}
    if not self.proxies:
      delete = requests.delete("http://{}:{}/api/dashboards/db/{}".format(self.server, self.port, dashboard), headers=hds)
    else:
      delete = requests.delete("http://{}:{}/api/dashboards/db/{}".format(self.server, self.port, dashboard), headers=hds, proxies=self.proxies)
    print delete.text

#if __name__ == "__main__":
#  gm = GrafanaManager("localhost",3000)
  # Uncomment to enable API requests through proxy
  #gm.proxies = {'http':'http://localhost:8080','https':'https://localhost:8443'}
#  gm.Login("admin","admin")
  #gm.EnablePlugin("alexanderzobnin-zabbix-app")
  #gm.zbx_user = "admin"
  #gm.zbx_pswd = "zabbix"
  #gm.zbx_url = "http://localhost/api_jsonrpc.php"
  #gm.CreateDatastore("Zabbix")
#  gm.ImportDashboard("./oim_dashboard.json")
