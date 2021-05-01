#  Fluent Bit - Data Observability Platform

![ Show image of grafana dashboard using supported Prometheus metric types](https://github.com/neiman-marcus/fluent-bit-data-observability-platform/blob/staging/out-prometheus-metrics-dashboard.png "Demo grafana dashboard showing supported Prometheus metric types")


## Purpose
This project provides a full data observability platform made up of a combination 
of several flagship CNCF log and metrics projects in the form of a single 
docker-compose environment.  
* Grafana - Data visualization UI
* Grafana Loki - Log aggregation system
* Prometheus Metrics - Systems and service monitoring system
* Fluent Bit - Data ingestion endpoint

This is a miniature version of a much larger cluster 
of containers we have hosted in the cloud.  

## What is it used for?
* Testing, experimentation, and 
debugging configurations prior to deploying into production
* A learning tool for getting up to speed on how the larger environment works 
* Grafana dashboard development sandbox environment
* Develop and test custom Fluent Bit configurations

**Reference Talk:** 
* [FluentCon 2021: Fluent Bit - Swiss Army Tool of Observability Data Ingestion](https://sched.co/iKok)
* [Fluent Bit Prometheus Metrics Output Plugin](https://github.com/neiman-marcus/fluent-bit-out-prometheus-metrics)

My hope is that the wider community will find this equally useful.

I plan to add a component to make it easy to switch between configuration sets and to start an archive of configurations in this project.

---
## Using the demo environment
#### Requirements:
* Either Docker Desktop, or docker and docker-compose.
* Make
* Curl

#### Note:
* Initial build time could be approximately 10-20min. Subsequent builds leverage cached local containers.
### Quick start
```
make all
```

### Build instructions
```
make build
```

### Start Prometheus Push Gateway and Fluent bit
```
make start
```

### Show current metrics
Execute repeatedly to see the metrics generated using the plugin.
```
make show-metrics
```

### Show current logs
Execute repeatedly to see the latest container logs
```
make logs
```

### Stop both containers
Shutdown demo environment.
```
make stop
```

### Persistent Storage
The docker-compose.yml file is configured for persistent storage.
To disable this, consider using docker-compose-non_persistent.yml.  Copy the desired version to docker-compose.yml and re-run: 
```
make build
```

---
### Local Web Access
Grafana
* http://localhost:3000/
  
Dashboards:
  
* Fluent Bit Prometheus Metrics Plugin
  * Dashboard pictured at the top of this page.  Let it run for 30-60min it will auto-populate using data 
    being sent by the nlog container.
* Data Observability Dashboard
  * Text panel with frequently accessed links

Prometheus Expression Browser
* http://localhost:9090/graph

PushGateway
* http://localhost:9091/

AlertManager
* http://localhost:9093/


### Projects referenced above:
https://fluentbit.io/
<br>
https://grafana.com/oss/grafana/
<br>
https://grafana.com/oss/loki/
<br>
https://prometheus.io/





# Authors

* [**Michael Marshall**](mailto:michael_marshall@neimanmarcus.com) - Project creation and development.
* [**Leon Cowle**](mailto:leon_cowle@neimanmarcus.com) - Nlog test harness developer.

## Conduct / Contributing / License

* Refer to our contribution guidelines to contribute to this project. See [CONTRIBUTING.md](https://github.com/neiman-marcus/nmg-sonarqube/tree/master/CONTRIBUTING.md).
* All contributions must follow our code of conduct. See [CONDUCT.md](https://github.com/neiman-marcus/nmg-sonarqube/tree/master/CONDUCT.md).
* This project is licensed under the Apache 2.0 license. See [LICENSE](https://github.com/neiman-marcus/nmg-sonarqube/tree/master/LICENSE).

## Acknowledgments
Thank you to the teams who create and maintain the individual projects listed above.