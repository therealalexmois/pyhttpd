#!/bin/bash

URL="http://127.0.0.1:8080/index.html"

echo "Starting load tests on $URL"

echo "Running Apache Benchmark (ab)..."
ab -n 1000 -c 10 "$URL"

echo "Running WRK..."
wrk -t12 -c400 -d30s "$URL"

echo "Load testing complete."
