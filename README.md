# packing_list
A simple package indexer

A simple package indexer. API details withheld for the moment.
Tested with python 3.5.

To run, clone the repo, cd into it, then build the dockerfile:
docker build -t packing_list .
And run the dockerfile:
docker run -d --name packing_list_app -p 8080:8080 packing_list
This will launch the service on port 8080.
