# Maki Model
Containerized implementation of [EASE](https://arxiv.org/abs/1905.03375) served over gRPC.

This service can run both in serve mode and train mode. In serve mode this component
listens to gRPC requests to generate anime recommendations and watches for checkpoint changes.
When a change in the model checkpoint file is detected the model is refreshed from disk.

In train mode, this component periodically retrains the model and stores the checkpoint on disk. **Note:** its required that the directory where checkpoints is the same! So be careful when writing deployment configurations!


For deployment and general information refer to the [main repository](https://github.com/maki-recommender/maki).


## Configuration

This section lists the environment variables that used to configure this service. 
Variables without a default value must be assigned.

`MAKI_IsRetrainer`

**Description:** Set to true to 

**Default:** 

`MAKI_PersistentPath`

**Description:** Path where model checkpoints are loaded/stored

**Default:** "data/"

---

`MAKI_ModelHost`

**ReTrainer mode enabled:** false 

**Description:** Server and port where gRPC listens to incoming connections

**Default:** "[::]:50051"


`MAKI_ModelWorkers`

**ReTrainer mode enabled:** false

**Description:** Number of workers serving gRPC requests 

**Default:** 10

---


`MAKI_PostgresUrl`

**ReTrainer mode enabled:** true


**Description:** PostgreSQL database connection required to read store anime list and update the model.

**Example:** "host={ip} user={username} password={password} dbname=maki port={port}"


`MAKI_RetrainEverySeconds`

**ReTrainer mode enabled:** true

**Description:** Time between following model retrains in seconds

**Default:** 604800 (7 days)



## Compiling the protocol

This section can be skipped unless some changes to the proto files need to be implemented in the application.

After installing the `requirements.dev.txt` dependencies run:

```bash
mkdir proto

python -m grpc_tools.protoc -I=./protos --python_out=./proto --pyi_out=./proto --grpc_python_out=./proto recommend_service.proto
```

