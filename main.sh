#!/bin/bash

echo "Generating static site..."
python3 src/main.py

echo "Starting server at http://localhost:8888"
cd public && python3 -m http.server 8888
