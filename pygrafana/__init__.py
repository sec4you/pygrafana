#!/usr/bin/python2.7

# Copyrights (c) Sec4You Consulting.

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
    self.mysql_host = ""
    self.mysql_port = ""
    self.mysql_db = ""
    self.mysql_user = ""
    self.mysql_pswd = ""

  def EnablePlugin(self,plugin):
    jdata = '{"enabled":true,"pinned":true,"jsonData":null}'
    jdata = yaml.load(jdata)
    enable = requests.post("{}/api/plugins/{}/settings".format(self.server,plugin),json=jdata, proxies=self.proxies, verify=self.verify)
    return enable.text

  def CreateDatastore(self,datastore):
    #Datastores supported:
    # - zabbix
    if datastore == "Zabbix":
      jdata = '{{"name":"Zabbix","type":"alexanderzobnin-zabbix-datasource","url":"{}","access":"direct","jsonData":{{"dbConnection":{{"enable":false}},"username":"{}","password":"{}"}},"secureJsonFields":{{}},"isDefault":true}}'.format(self.zbx_url,self.zbx_user,self.zbx_pswd)
      jdata = yaml.load(jdata)
      enable = requests.post("{}/api/datasources".format(self.server),json=jdata, proxies=self.proxies, verify=self.verify)
      return enable.text
    elif datastore == "MySQL":
      jdata = '{{"name":"MySQL","type":"mysql","url":"{}:{}","access":"proxy","jsonData":{{}},"secureJsonFields":{{}},"user":"{}","password":"{}","database":"{}"}}'.format(self.mysql_host, self.mysql_port, self.mysql_user, self.mysql_pswd, self.mysql_db)
      jdata = yaml.load(jdata)
      enable = requests.post("{}/api/datasources".format(self.server),json=jdata, proxies=self.proxies, verify=self.verify)
      return enable.text
    else:
      return "Datastore not supported."

  def ImportDashboard(self,dashboard):
    dash = '{"dashboard":'+ open(dashboard,"r").read() + '}'
    if self.oim_server:
      dash.replace("<SERVER>",self.oim_server)
    jdata = yaml.load(dash)
    imprt = requests.post("{}/api/dashboards/db".format(self.server),json=jdata, proxies=self.proxies, verify=self.verify)
    return imprt.text

  def StarDashboard(self, id):
    star = requests.post("{}/api/user/stars/dashboard/{}".format(self.server,id),proxies=self.proxies, verify=self.verify)
    return star.text

  def DeleteDashboard(self, dashboard):
    delete = requests.delete("{}/api/dashboards/db/{}".format(self.server, dashboard), proxies=self.proxies, verify=self.verify)
    return delete.text

  def ChangeTheme(self, theme):
    change = requests.put("{}/api/user/preferences".format(self.server),data={"theme":"{}".format(theme),"timezone":"","homeDashboardId":""})
    return change.text

  def CreateOrganization(self, name):
    create = requests.post("{}/api/orgs".format(self.server),data={"name":"{}".format(name)})
    return create.text

#  def DefaultDashboard(self, id):
#    #NOT WORKING
#    jdata = {"theme":"","timezone":"","homeDashboardId":int(id)}
#    print jdata
#    default = requests.put("{}/api/org/preferences".format(self.server),data=jdata)
#    print default.text

# === Change log:
#
# 2017, Sep, Angelo Moura
#    - Changed self.oim_server from os.getenv to a string
#    - Removed unecessary imports
#    - Added Star Dashboard Method
#    - Added Change Theme Method


