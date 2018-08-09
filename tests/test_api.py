import requests
import httpretty
import json
import os
from pygrafana import GrafanaManager

gm = GrafanaManager("http://grafana")

gm.zbx_user = "admin"
gm.zbx_pswd = "zabbix"
gm.zbx_url = "http://localhost/api_jsonrpc.php"
gm.mysql_host = "mysql-server"
gm.mysql_port = "3306"
gm.mysql_db = "database"
gm.mysql_user = "user"
gm.mysql_pswd = "password"

# EnablePlugin
@httpretty.activate
def test_one():
  httpretty.register_uri(httpretty.POST, "http://grafana/api/plugins/alexanderzobnin-zabbix-app/settings",
    body=json.dumps(
      {"message":"Plugin settings updated"}
    ),
  )
  test_1 = gm.EnablePlugin("alexanderzobnin-zabbix-app")
  assert test_1 == '{"message": "Plugin settings updated"}'

# CreateDatastore
@httpretty.activate
def test_two():
  Systems = ["Zabbix","MySQL"]
  for i in Systems:
    httpretty.register_uri(httpretty.POST, "http://grafana/api/datasources",
      body='{{"id":1,"message":"Datasource added","name":"{}"}}'.format(i)
    )
    test_2 = gm.CreateDatastore(i)
    response = '{{"id":1,"message":"Datasource added","name":"{}"}}'.format(i)
    assert test_2 == response

# ImportDashboard
@httpretty.activate
def test_three():
  httpretty.register_uri(httpretty.POST, "http://grafana/api/dashboards/db",
    body='{"slug":"template-linux-server","status":"success","version":1}'
  )
  test_3 = gm.ImportDashboard(os.path.join(os.path.dirname(__file__),'test_dashboard.json'))
  assert test_3 == '{"slug":"template-linux-server","status":"success","version":1}'

# StarDashboard
@httpretty.activate
def test_four():
  httpretty.register_uri(httpretty.POST, "http://grafana/api/user/stars/dashboard/1",
    body='{"message":"Dashboard starred!"}'
  )
  test_4 = gm.StarDashboard(1)
  assert test_4 == '{"message":"Dashboard starred!"}'

# DeleteDashboard
@httpretty.activate
def test_five():
  httpretty.register_uri(httpretty.DELETE, "http://grafana/api/dashboards/db/dashboard",
    body='{"title":"Dashboard"}'
  )
  test_5 = gm.DeleteDashboard("dashboard")
  assert test_5 == '{"title":"Dashboard"}'

# ChangeTheme
@httpretty.activate
def test_six():
  httpretty.register_uri(httpretty.PUT, "http://grafana/api/user/preferences",
    body='{"message":"Preferences updated"}'
  )
  test_6 = gm.ChangeTheme("light")
  assert test_6 == '{"message":"Preferences updated"}'


@httpretty.activate
def test_seven():
  httpretty.register_uri(httpretty.POST, "http://grafana/api/orgs",
    body='{"message":"Organization created","orgId":2}'
  )
  test_7 = gm.CreateOrganization("Cliente1")
  assert test_7 == '{"message":"Organization created","orgId":2}'

test_one()
test_two()
test_three()
test_four()
test_five()
test_six()
test_seven()