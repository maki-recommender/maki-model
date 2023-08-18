# Maki brain
Containerized implementation of [EASE](https://arxiv.org/abs/1905.03375) served over gRPC.

## Getting started

WIP

Environment variables:
-
-

## Compoling the protocol

This section can be skipped unless some changes to the proto files need to be implemented in the application.

After installing the `requirements.dev.txt` dependencies run:

```bash
mkdir proto

python -m grpc_tools.protoc -I=./protos --python_out=./proto --pyi_out=./proto --grpc_python_out=./proto recommend_service.proto
```

