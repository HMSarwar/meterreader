# meterreader
A simple gRPC app

### command for generating code from .proto
$ python -m grpc_tools.protoc -I../protobufs --python_out=. --grpc_python_out=. ../protobufs/meterreader.proto


### Short Overview
1. gRPC server for serving data reading from csv file with time range filter
2. gRPC client for communicating with gRPC server
3. Simple Flask app to take time range input from users and providing json response


### How to run the project

1. Install Python > 3.6
2. Install the requirements from requirements.txt -> pip install -r requirements.txt
3. change directory to meter reader cd meterreader
4. for gRPC server run: python meter_reader_server.py
5. for gRPC client and flask app run: pyton data_server.py

the gRPC server runs @ 127.0.0.1:5005
You can hit 127.0.0.1:4455 for date range search and the server will provide
 json response of the filtered data

