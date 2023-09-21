# Backend

## docker-runner

> [!NOTE]  
> Before getting started please make sure you have provided necessary permissions for the `./scripts/docker-runner.sh` script.
> You can do this by running the following command: `chmod +x scripts/docker-runner.sh`

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

> **Note:** The `-d` flag is used to run the containers in the background.
> If you want to run the containers in the foreground, use `-r` flag instead.
> It is recommended to run the containers in the background. You can view the
> logs of the containers using the `-l` flag.

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

#### Help
To view the help menu, run the following command:
```bash
./scripts/docker-runner.sh -h
```

--------------------------------------------

## Database Setup

> [!NOTE]
> Before getting started please make sure you have provided necessary permissions for the `./scripts/create_pgdb.sh` script.
> You can do this by running the following command: `chmod +x scripts/create_pgdb.sh`. And also make sure you have installed 
> postgresql in your system.

The `create_pgdb.sh` script is used to setup the postgres database for the backend. The script can be
used to setup the following:
1. Create a new postgres user
2. Create a new database

#### Setup
To setup the postgres database, run the following command:
```bash
./scripts/create_pgdb.sh
```
> **Note:** The script runs superuser commands. You will be prompted to enter your password.

--------------------------------------------

## Running the server

> [!NOTE]
> Before getting started please make sure you have provided necessary permissions for the `./scripts/start_server.sh` script.
> You can do this by running the following command: `chmod +x scripts/start_server.sh`.

```bash
./scripts/start_server.sh
```
