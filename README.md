# pygrafana

Python Library to consume Grafana's API.


## Instalation
```
$ sudo pip install pygrafana
```

## First - Login into Grafana

```
>>> from pygrafana import GrafanaManager
>>> gm = GrafanaManager("localhost",3000)
>>> gm.Login("admin","admin")
```

## Create Zabbix Datastore

### TO-DO, fill parameters of other datastore types

```
>>> gm.zbx_user = "admin"
>>> gm.zbx_pswd = "zabbix"
>>> gm.zbx_url = "http://localhost/api_jsonrpc.php"
>>> gm.CreateDatastore("Zabbix")
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

## Through Proxy

```
>>> gm.proxies = {'http':'http://localhost:8080','https':'https://localhost:8443'}
```

## Examples

- **Example 1**: Auto-configuring Grafana-Zabbix API and importing a dashboard.
```
#!/usr/bin/python2.7
from pygrafana import GrafanaManager
gm = GrafanaManager("localhost",3000)
gm.Login("admin","admin")
gm.EnablePlugin("alexanderzobnin-zabbix-app")
gm.zbx_user = "admin"
gm.zbx_pswd = "zabbix"
gm.zbx_url = "http://localhost/api_jsonrpc.php"
gm.CreateDatastore("Zabbix")
gm.ImportDashboard("./zabbix_dashboard.json")
```
