# SonarQube Installation Log

**Date:** 05-Aug-2026  
**Time:** 12:24:27 PM  
**Software:** SonarQube Community Edition 25.7  
**Operating System:** Ubuntu Linux

---

## SonarQube Startup Log

```log
2026.08.05 12:24:27 INFO  app[][o.s.a.AppFileSystem]
Cleaning or creating temp directory:
    /opt/sonarqube/temp

2026.08.05 12:24:27 INFO  app[][o.s.a.es.EsSettings]
Elasticsearch listening on:
    HTTP : 127.0.0.1:9001
    TCP  : 127.0.0.1:{}

2026.08.05 12:24:27 INFO  app[][o.s.a.ProcessLauncherImpl]
Launching Elasticsearch process from:
    /opt/sonarqube/elasticsearch

Java Runtime:
    /usr/lib/jvm/java-17-openjdk-amd64/bin/java

Memory Configuration:
    Initial Heap (-Xms): 4 MB
    Maximum Heap (-Xmx): 64 MB

Status:
    Elasticsearch process started successfully.

2026.08.05 12:24:27 INFO  app[][o.s.a.SchedulerImpl]
Waiting for Elasticsearch to become available...

2026.08.05 12:24:48 INFO  app[][o.s.a.SchedulerImpl]
Process [ELASTICSEARCH] is up and running.

2026.08.05 12:24:48 INFO  app[][o.s.a.ProcessLauncherImpl]
Launching SonarQube Web Server

Java Runtime:
    /usr/lib/jvm/java-17-openjdk-amd64/bin/java

Web Server Memory:
    Initial Heap (-Xms): 128 MB
    Maximum Heap (-Xmx): 512 MB

Database Driver:
    H2 Database
    /opt/sonarqube/lib/jdbc/h2/h2-2.3.232.jar

Status:
    SonarQube Web Server started successfully.
```

---

## Startup Summary

| Component | Status |
|-----------|--------|
| Temporary Directory | ✅ Created |
| Elasticsearch | ✅ Started Successfully |
| Scheduler | ✅ Running |
| Web Server | ✅ Started Successfully |
| Java Runtime | OpenJDK 17 |
| Database | H2 Embedded Database |

---

## Conclusion

The SonarQube Community Edition startup completed successfully. Elasticsearch initialized correctly, the scheduler detected the running Elasticsearch service, and the SonarQube Web Server launched without errors using Java 17 and the embedded H2 database.
