# Backend

## docker-runner
The `docker-runner.sh` script is used to setup the docker containers for the backend. The script can be 
used to setup the following containers:
1. Elasticsearch
2. Kibana
3. Logstash

While running for the first time the `base_dataset.csv` will be loaded into elasticsearch as an index.
The index name is `plants`. 

You can configure your kibana configurations in the `docker/kibana.yml` file and 
the logstash configurations in the `docker/logstash.conf` file.


#### Setup | Start
To setup the elasticsearch, kibana and logstash docker containers, run the following command:
```bash
./scripts/docker-runner.sh -d elk
```

After the initial setup, a new directory will be created in the docker directory
called `logstash_data`. This directory will contain the logstash data. This directory will be mounted to 
the logstash container. This will ensure that the data is not lost when the container is stopped.

You can use the following ports to access the services: `http://localhost:<port>`
1. Elasticsearch - 9200
2. Kibana - 5601
3. Logstash - 9600

#### Stop
To stop the containers, run the following command:
```bash
./scripts/docker-runner.sh -s elk
```

#### Logs
To view the logs of the containers, run the following command:
```bash
./scripts/docker-runner.sh -l elk
```