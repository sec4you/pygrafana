# pygrafana

Python Module to consume Grafana's API.


## Instalation
```
$ sudo pip install pygrafana
```

## Login into Grafana

```
URL = http://<USERNAME>:<PASSWORD>@<SERVER>:<PORT>
>>> from pygrafana import GrafanaManager
>>> gm = GrafanaManager("http://admin:admin@localhost:3000")
```

## Create Datastore

> TO-DO: Add all the Datastore types

Supported Datastores by now:
 - Zabbix
 - MySQL

### Zabbix
```
>>> gm.zbx_user = "admin"
>>> gm.zbx_pswd = "zabbix"
>>> gm.zbx_url = "http://localhost/api_jsonrpc.php"
>>> gm.CreateDatastore("Zabbix")
```

### MySQL
```
>>> gm.mysql_host = "10.0.0.1"
>>> gm.mysql_port = "3306"
>>> gm.mysql_db = "database1"
>>> gm.mysql_user = "user"
>>> gm.mysql_pswd = "password"
>>> gm.CreateDatastore("MySQL")
```

## Import Dashboard

```
>>> gm.ImportDashboard("./example_dashboard.json")
```


## Delete Dashboard
```
>>> gm.DeleteDashboard("example-dashboard")
```


## Enable Plugin

```
>>> gm.EnablePlugin("alexanderzobnin-zabbix-app")
```


## Change Grafana's Theme

```
>>> gm.ChangeTheme("light")
```


## Star a Dashboard

```
>>> gm.StarDashboard("3")
```

## Create an Organization

```
>>> gm.CreateOrganization("OrganizationName")
```



## Through Proxy

```
>>> gm.proxies = {'http':'http://localhost:8080','https':'https://localhost:8443'}
```


## Examples

- **Example 1**: Auto-configuring Grafana-Zabbix API and importing a dashboard.
```
#!/usr/bin/python2.7
from pygrafana import GrafanaManager
gm = GrafanaManager("http://admin:admin@localhost:3000")
gm.EnablePlugin("alexanderzobnin-zabbix-app")
gm.zbx_user = "admin"
gm.zbx_pswd = "zabbix"
gm.zbx_url = "http://localhost/api_jsonrpc.php"
gm.CreateDatastore("Zabbix")
gm.ImportDashboard("./zabbix_dashboard.json")
```
