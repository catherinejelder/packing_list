# packing_list

A simple package indexing service. API details withheld for the moment.
Tested on ubuntu.

To run, pull the docker image from Docker Hub:
```bash
docker pull catherinejelder/packing_list
```
And run the dockerfile:
```bash
docker run -d --name packing_list_app -p 8080:8080 catherinejelder/packing_list
```
This will launch the service on port 8080.
