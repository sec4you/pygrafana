#!/usr/bin/python2.7

# Copyrights (c) Sec4You Consulting.

# === Change log:
#
# 2017, Sep, Angelo Moura
#    - Changed self.oim_server from os.getenv to a string
#    - Removed unecessary imports

import requests
import yaml

class GrafanaManager(object):
  def __init__(self, server):
    self.server = server
    self.proxies = False
    self.verify = False

    self.zbx_user = ""
    self.zbx_pswd = ""
    self.zbx_url = ""

    self.oim_server = ""

  def EnablePlugin(self,plugin):
    jdata = '{"enabled":true,"pinned":true,"jsonData":null}'
    jdata = yaml.load(jdata)
    enable = requests.post("{}/api/plugins/{}/settings".format(self.server,plugin),json=jdata, proxies=self.proxies, verify=self.verify)
    print enable.text

  def CreateDatastore(self,datastore):
    #Datastores supported:
    # - zabbix
    if datastore == "Zabbix":
      jdata = '{{"name":"Zabbix","type":"alexanderzobnin-zabbix-datasource","url":"{}","access":"direct","jsonData":{{"dbConnection":{{"enable":false}},"username":"{}","password":"{}"}},"secureJsonFields":{{}},"isDefault":true}}'.format(self.zbx_url,self.zbx_user,self.zbx_pswd)
      jdata = yaml.load(jdata)
      enable = requests.post("{}/api/datasources".format(self.server),json=jdata, proxies=self.proxies, verify=self.verify)
      print enable.text
    else:
      print "Datastore not supported."

  def ImportDashboard(self,dashboard):
    dash = '{"dashboard":'+ open(dashboard,"r").read() + '}'
    if self.oim_server:
      dash.replace("<SERVER>",self.oim_server)
    jdata = yaml.load(dash)
    enable = requests.post("{}/api/dashboards/db".format(self.server),json=jdata, proxies=self.proxies, verify=self.verify)
    print enable.text


  def DeleteDashboard(self, dashboard):
    delete = requests.delete("{}/api/dashboards/db/{}".format(self.server, dashboard), proxies=self.proxies, verify=self.verify)
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
